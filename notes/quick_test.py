# %%
import re, json

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

def merge_adjacent_like_elements(o_parent:list=[]) -> list:
    """
    loop over the elements and any elements which are adjacent and the same type should 
    be merged
    """
    new_parent = []
    current_child = o_parent[0]
    for next_child in o_parent[1:]:
        # to merge adjacent values, they need to have the same token type, and they both must bold string values
        if current_child[0] == next_child[0] and isinstance(current_child[1], str) and isinstance(next_child[1], str) :
            current_child[1] = current_child[1] + next_child[1]
            next_child[0] = "merged"
        else:
            # only swap children if they do not match
            new_parent.append(current_child)
            current_child = next_child
    # add the final child 
    new_parent.append(current_child)
    return new_parent


def check_merge_parent(parent, bank):
    if len(parent[1]) == 1:
        only_child = parent[1].pop()
        if only_child[0] == "text":
            parent[1] = only_child[1]
            bank.pop()
        else:
            parent[1] = only_child

def parse_inline_tokens(tokens):
    depth = 0
    tracker = {}
    object_stack = []
    token_stack = []
    bank = []
    root = ["root", []]
    current_parent = root
    
    KEY_TOKEN = 0
    KEY_DATA = 1
    
    for token, value, nestable in tokens:
        print(f"{token}-------------------------------")
        
        
        if not nestable:
            new_child = [token, value]
            bank.append(new_child)
            current_parent[KEY_DATA].append(new_child)
        else:
            if token not in tracker:
                tracker[token] = False
            # flip the switch
            tracker[token] = not tracker[token]
            # if the token is open
            if tracker[token]:
                # new open token, increase the depth
                depth+=1
                # create a new object
                new_parent = [token, []]
                bank.append(new_parent)
                # add the new object as a child to the current object
                current_parent[KEY_DATA].append(new_parent)
                # add the current object to the stack
                object_stack.append(current_parent)
                # assign the new object as the current object
                current_parent = new_parent
                token_stack.append(token)
            else:
                # if the token is closed
                # when we close a formatting context, we need change parents
                if depth and len(object_stack):
                    expected_token = token_stack.pop()
                    if token == expected_token:
                        #current_parent[KEY_TOKEN] = token
                        # if there is only one child element, just make that one child equal to it
                        check_merge_parent(current_parent, bank)
                        #if len(current_parent[KEY_DATA]) == 1:
                        #    single_child = current_parent[KEY_DATA].pop()
                        #    if single_child[KEY_TOKEN] == "text":
                        #        current_parent[KEY_DATA] = single_child[KEY_DATA]
                        #        bank.pop()
                        #    else:
                        #        current_parent[KEY_DATA] = single_child
                        # update current parent
                        current_parent = object_stack.pop()
                        depth-=1
                    else:
                        # if the expected token does not equal the currrent token
                        # we need to change levels. 
                        while token != expected_token:
                            current_parent = object_stack.pop()
                            previous_child = current_parent[KEY_DATA].pop()
                            current_parent[KEY_DATA].extend(previous_child[KEY_DATA])
                            current_parent[KEY_DATA] = merge_adjacent_like_elements(current_parent[KEY_DATA])
                            check_merge_parent(current_parent, bank)
                            expected_token = token_stack.pop()
                            depth-=1
                            
                        current_parent = object_stack.pop()
                        depth-=1    
                #depth-=1
                
        print(json.dumps(root[KEY_DATA], indent=4))
        
    # before merging 
    print("Before merging-------------------------------")
    print(json.dumps(root[KEY_DATA], indent=4))
    
    # so if we still have depth
    # that means we havent closed one of our boundaries
    while depth:
        if len(object_stack):
            # grab the previous parent
            previous_parent = object_stack.pop()
            # remove the previous child from the previous parents list
            #print(previous_child)
            previous_child = previous_parent[KEY_DATA].pop()
            #print(f"depth: {depth}")
            #print(json.dumps(previous_child, indent=4))
            if len(previous_child[KEY_DATA]) > 1:
                previous_child[KEY_DATA] = merge_adjacent_like_elements(previous_child[KEY_DATA])
            # take the list from teh previous child and merge it with the previous parents
            previous_parent[KEY_DATA].extend(previous_child[KEY_DATA])
        depth-=1
        #break
    root[KEY_DATA] = merge_adjacent_like_elements(root[KEY_DATA])

    # we can make edits here that will reflect in our final tree
    bank = [_ for _ in bank if isinstance(_[KEY_DATA], str) and _[KEY_TOKEN] != "merged"]
    
    print("After merging-------------------------------")
    print(json.dumps(root[KEY_DATA], indent=4))
    
    return root[KEY_DATA]

# %%
"""
18:21 03/10/2024
the bug we have right now is that we cant have mismatched nested tags. 
tags that are opened inside of other tags need to be closed before the other tags can be
"""

MD_LIST = [
    "Before 01 **middle content** after 01.",
    "Before 02 __middle content__ after 02.",
    "Before 03 _middle content_ after 03.",
    "Before 04 *middle content* after 04.",
    "Before 05 ^middle content^ after 05.",
    "Before 06 ~middle content~ after 06.",
    "Before 07 ~~middle content~~ after 07.",
    "Before 08 --middle content-- after 08.",
    "Before 09 ==middle content== after 09.",
    "Before 10 ``middleContent`` after 10.",
    "Before 11 :middle_content: after 11.",
    "Before 12 `middleContent` after 12.",
    "Before 13 <https://www.markdownguide.org> after 13.",
    "Before 14 [^1] after 14.",
    "Before 15 [link to Markdown documentation](https://www.markdownguide.org) after 15.",
    "Before 16 <navlink>middle content</navlink> after 16.",

    ## nesting
    #"Before 01 **middle `nested stuff content** after 01.",
    #"Before 02 __middle `nested stuff content__ after 02.",
    #"Before 03 _middle `nested stuff content_ after 03.",
    #"Before 04 *middle `nested stuff content* after 04.",
    #"Before 05 ^middle `nested stuff content^ after 05.",
    #"Before 06 ~middle `nested stuff` content~ after 06.",
    #"Before 07 ~~middle `nested stuff` content~~ after 07.",
    #"Before 08 --middle `nested stuff` content-- after 08.",
    #"Before 09 ==middle `nested stuff` content== after 09.",
    #"Before 10 ``middle `nested stuff` Content`` after 10.",
    #"Before 11 :middle_content: after 11.",
    #"Before 12 `middleContent` after 12.",
    #"Before 13 <https://www.markdownguide.org> after 13.",
    #"Before 14 [^1] after 14.",
    #"Before 15 [link to Markdown documentation](https://www.markdownguide.org) after 15.",
    #"Before 16 <navlink>middle content</navlink> after 16.",
    
    ## larger
    #"***Markdown Example** with* nesting and `inline code` and more *nested italics* at the end.",
    #"How about some **unbalanced _markdown and `some code`.",
    #"How about some **unbalanced _markdown.",
    #"How about some **strong _emphasised --deleted ^super ==marked ~sub content as well",
    """**Markdown Example** with _**Inline Markup**_.,
    This is a **bold** statement, and this is an _italicized_ one.
    You can even combine them to make text _**both italic and bold**_.
    This item has some inline markup like _italics_ and **bold** text.
    Even deeper nesting: _Italicized_ **bold** list item with `code` inline.
    Another item with **nested** inline **markup**.
    This list item uses some ``inline sample codee`` and ends with _**italicized and bold**_ text.
    To write code, you can use backticks for `inline code`, like this.
    This is some **double nested _italicised markdown_ where we nest multiple `different` times** in one line.
    Random footnote[^1] near the end.""",
]
MD = " ".join(MD_LIST)

MD = """Before 01 **middle `nested stuff content** after 01."""

tokens = scanner.scan(MD)
#for token,value, nestable in tokens:
#    print(f"{token} | {value}")
converted = parse_inline_tokens(tokens)
#converted = list(filter(lambda x: x[0] != "text", converted))
print("done ------------------------------")
print(json.dumps(converted, indent=4))


# %%
