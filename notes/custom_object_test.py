# %%
import re, json

class Parent:
    __slots__ = ['type', 'children']
    
    def __init__(self, formattype, children:list=[]):
        self.type = formattype
        self.children = []
        if children:
            self.children = children
            
    @property
    def has_children(self):
        return isinstance(self.children, list) and len(self.children)
    
    def to_dict(self):
        if isinstance(self.children, list) and len(self.children) == 1:
            self.children = self.children.pop()
        return [self.type, self.children]
    
    def add_child(self, child):
        if self.has_children:
            last_child = self.children[-1]
            # merge kids if they are the same type
            if last_child.type == child.type and isinstance(last_child.children, str) and isinstance(child.children, str) :
                last_child.children = last_child.children + child.children
                return
        self.children.append(child)
        return
                
    def add_children(self, children:list=[]):
        for child in children:
            self.add_child(child)
        
    def remove_last_child(self):
        return self.children.pop()

    def get_representation(self):
        if self.has_children:
            if len(self.children) == 1:
                if self.children[0].type == "text":
                    return [self.type, self.children[0].children]
                return [self.type, self.children[0].get_representation()]
            else:
                return [self.type, [_.get_representation() for _ in self.children]]
        # if the children is a string
        elif isinstance(self.children, str):
            return [self.type, self.children]
        # if the children are a list
        else:
            return [self.type, self.children.get_representation()]    
        
    #def get_representation(self):
    #    # if the children is a string
    #    if isinstance(self.children, str):
    #        return [self.type, self.children]
    #    # if the children are a list
    #    elif isinstance(self.children, list):
    #        if len(self.children) == 1:
    #            self.children = self.children.pop()
    #            return [self.type, self.children.get_representation()]
    #        else:
    #            return [self.type, [_.get_representation() for _ in self.children]]
    #    else:
    #        return [self.type, self.children.get_representation()]    

class ParentStack:
    __slots__ = ['data', 'tracker']
    
    def __init__(self):
        self.data = []
        self.tracker = []
    
    def add_to_stack(self, x:Parent):
        self.tracker.append(x.type)
        self.data.append(x)
        
    def remove_from_stack(self) -> Parent:
        self.tracker.pop()
        return self.data.pop()
    
    def check_in(self, key:str="") -> bool:
        return key in self.tracker
    

class ScannerGenerator(re.Scanner):
    def scan(self, string):
        text_group = []
        match = self.scanner.scanner(string).match
        i = 0
        while True:
            m = match()
            if not m:
                # no match, break and return string
                break
            j = m.end()
            if i == j:
                # set j to the end of the match
                # if i is equal to j, we have matched
                # at the end again so break
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                # (token, value, nestable)
                self.match = m
                ret  = action(m.group())
                if ret[0] == "text":
                    text_group.append(ret[1])
                else:
                    if len(text_group):
                        yield ["text", "".join(text_group), False]
                    text_group = []
                    yield ret
            # set i to j so we know
            # we are moving along the string
            i = j
        text_group.append(string[i:])
        yield ["text", "".join(text_group), False]

"""
the lambda receive the value of the token
the lambda should return, in order
label, token value, if the token can be nested
"""
scanner = ScannerGenerator([
    (r"(?:\*\*)|(?:__)", lambda t: ["strong", t, True]),
    (r"(?:\~\~)|(?:\-\-)", lambda t: ["del", t, True]),
    (r"\=\=", lambda t: ["mark", t, True]),
    (r"\^(?=[^\^])", lambda t: ["sup", t, True]),
    (r"\~(?=[^\~])", lambda t: ["sub", t, True]),
    (r"(?:\*)|(?:_)", lambda t: ["em", t, True]),
    (r"``", lambda t: ["samp", t, True]),
    (r"`", lambda t: ["code", t, True]),
    
    #(r"``.+?``", lambda t: ["samp", t[2:-2], False]),
    #(r"\`.+?\`", lambda t: ["code", t[1:-1], False]),
    (r"\$.*?\$", lambda t: ["math", t, False]),
    (r"\:.*?\:", lambda t: ["emoji", t[1:-1], False]),
    (r"\[\^\d+\]", lambda t: ["footnote", t[2:-1], False]),
    (r"\[.*?\]\([^ ]+?\)", lambda t: ["link", t, False]),
    
    (r"\<(\S+)[^\>\<]*?\>.*?\<\/\1\>", lambda t: ["html", t, False]),
    (r"\<[^ ]+?\>", lambda t: ["rawlink", t[1:-1], False]),
    #(r"\w+", lambda t: ["text", t, True]),
    (r"[a-zA-Z0-9]+", lambda t: ["text", t, False]),
    (r"\s+", lambda t: ["text", t, False]),
    (r".+?", lambda t: ["text", t, False]),
])

# %%
def loop_and_merge_adjacent_like_elements(current_parent):
    """
    loop over the elements and any elements which are adjacent and the same type should 
    be merged
    """
    children = current_parent.children
    new_parent = []
    current_child = children[0]
    
    for next_child in children[1:]:
        # to merge adjacent values, they need to have the same token type, and they both must bold string values
        if current_child.type == next_child.type and isinstance(current_child.children, str) and isinstance(next_child.children, str) :
            current_child.children = current_child.children + next_child.children
            next_child.type = "merged"
        else:
            # only swap children if they do not match
            new_parent.append(current_child)
            current_child = next_child
            
    # add the final child 
    new_parent.append(current_child)
    current_parent.children = new_parent

def check_merge_parent(parent):
    """
    the parent normally has a bunch of kids
    however, if a parent has only one child, that child should
    be equal to the children property. 
    """
    if len(parent.children) == 1:
        child = parent.remove_last_child()
        if child.type == "text":
            parent.children = child.children
        else:
            parent.children = child

def parent_to_grandparent(stack):
    current_parent = stack.pop()
    previous_child = current_parent.remove_last_child()
    current_parent.add_children(previous_child.children)
    #loop_and_merge_adjacent_like_elements(current_parent)
    return current_parent

def initialise_new_parent(stack, parent, token):
    # new open token, create a new object
    new_parent = Parent(token)
    # add the new object as a child to the current object
    parent.add_child(new_parent)
    # add the current object to the stack
    stack.append(parent)
    return new_parent

def parse_inline_tokens(tokens):
    tracker = []
    object_stack = []
    root = Parent("root", [])
    current_parent = root
    
    for token, value, nestable in tokens:
        #print(f"{token}-------------------------------")
        if not nestable:
            if token == "text" and not len(value):
                continue
            new_child = Parent(token, value)
            current_parent.add_child(new_child)
        else:
            if token not in tracker:
                # assign the new object as the current object
                current_parent = initialise_new_parent(object_stack, current_parent, token)
                tracker.append(token)
            else:
                # if the token is closed
                # when we close a formatting context, we need change parents
                if len(object_stack):
                    # close the formatting context if the token matches
                    if token == current_parent.type:
                        # if there is only one child element, just make that one child equal to it
                        #check_merge_parent(current_parent)
                        pass
                    else:
                        # if the expected token does not equal the currrent token
                        # we need to change levels. 
                        while token != current_parent.type:
                            current_parent = parent_to_grandparent(object_stack)
                            tracker.pop()
                            #check_merge_parent(current_parent)
                            
                    current_parent = object_stack.pop()
                    tracker.pop()
    # so if we still have depth that means we havent closed one of our boundaries
    while len(object_stack):
        parent_to_grandparent(object_stack)
        
    #loop_and_merge_adjacent_like_elements(root)
    #return root.children
    return root.get_representation()[1]

# %%

MD_TEST_CASES = [
    ## regular
    ("**formatted content**", ["strong", "formatted content"]),
    ("before **in between** after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    ("before __in between__ after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    ("before _in between_ after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    ("before *in between* after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    ("before ^in between^ after", [["text", "before "], ["sup", "in between"], ["text", " after"]]),
    ("before ~in between~ after", [["text", "before "], ["sub", "in between"], ["text", " after"]]),
    ("before ~~in between~~ after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    ("before --in between-- after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    ("before ==in between== after", [["text", "before "], ["mark", "in between"], ["text", " after"]]),
    ("before ``in between`` after", [["text", "before "], ["samp", "in between"], ["text", " after"]]),
    ("before :in between: after", [["text", "before "], ["emoji", "in between"], ["text", " after"]]),
    ("before `in between` after", [["text", "before "], ["code", "in between"], ["text", " after"]]),
    ("before <https://in.between.org> after", [["text", "before "], ["rawlink", "https://in.between.org"], ["text", " after"]]),
    ("before [^1] after", [["text", "before "], ["footnote", "1"], ["text", " after"]]),
    ("before [in between](https://in.between.org) after", [["text", "before "], ["link", "[in between](https://in.between.org)"], ["text", " after"]]),
    ("before <navlink title=\"in between\">in between</navlink> after", [["text", "before "], ["html", "<navlink title=\"in between\">in between</navlink>"], ["text", " after"]]),
    
    ## single nesting
    ("before **in `nested content` between** after", [["text", "before "], ["strong", [["text", "in "], ["code", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ## double nesting
    ("before **in _nested `double nested` content_ between** after", [["text", "before "], ["strong", [["text", "in "], ["em", [["text", "nested "], ["code", "double nested"], ["text", " content"]]], ["text", " between"]]], ["text", " after"]]),
    ## order of operations
    ("before ==in **nested content** between== after", [["text", "before "], ["mark", [["text", "in "], ["strong", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ## unbalanced
    ("before **unbalanced _nested `content`**", [["text", "before "], ["strong", [["text", "unbalanced nested "], ["code", "content"]]]]),
    ## irregular nesting
    ("before **in `nested content between** after", [["text", "before "], ["strong", "in nested content between"], ["text", " after"]]),
    ## edge cases
    ("How about some **strong _emphasised --deleted ^super ==marked ~sub content as well", "How about some strong emphasised deleted super marked sub content as well"),
]

def custom_json_encoder(obj):
    if isinstance(obj, Parent):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")



for index, case in enumerate(MD_TEST_CASES):
    md, solution = case
    tokens = scanner.scan(md)
    answer = parse_inline_tokens(tokens)
    #answer = list(filter(lambda x: x[0] != "text", answer))
    if solution != answer:
        print(f"case {index} --------------------")
        print(f"failed")
        print("The Solution")
        print(solution)
        print("My Answer")
        print(answer)

#
#MD = """**Markdown Example** with _**Inline Markup**_. 
#This **_==`inline code`==_** and ends with _**italicized and bold**_ text. 
#Some __super *nested ==deep content `right here`== right now* duper__ yeet. 
#Going ~~in *and in* and out *and then in again* and then out~~ yeet."""
#
#tokens = scanner.scan(MD)
#ret = parse_inline_tokens(tokens)
#print(json.dumps(ret, indent=4, default=custom_json_encoder))
print("done ------------------------------")

# %%
