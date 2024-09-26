#%%
import re
from typing import Union, List

"""
pattern
key
symmetrical
"""
CASES = [
    ## symettrical
    [[("`", "`")], "code"],
    [[("**", "**"), ("__", "__")], "strong"],
    [[("*", "*"), ("_", "_")], "em"],
    [[("~~", "~~"), ("--", "--")], "del"],
    [[("==", "==")], "mark"],
    [[("``", "``")], "samp"],
    [[(":", ":")], "emoji"],
    [[("^", "^")], "sup"],
    [[("~", "~")], "sub"],
    [[("$", "$")], "math"],
    
    ## non symettrical
    [[("<navlink ", "</navlink>")], "navlink"],
    [[("<", ">")], "rawlink"],
    [[("[^", "]")], "footnote"],
    [[("[", ")")], "link"],
    #[(" ", " "), "text", True],
]

lambda_extractor = lambda pat: lambda x: x[len(pat[0]):len(pat[1])*(-1)]
lambda_formatter = lambda pat: lambda x: f"{pat[0]}{x}{pat[1]}"

# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})" 
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>

# processing content
get_text_captured = lambda cur, content: content[cur[0]:cur[1]]
get_text_between = lambda pre, cur, content: content[pre[1]:cur[0]]
get_text_after = lambda cur, content: content[cur[1]::]
create_text_object = lambda content: {"type": "text", "data": content}
create_markup_object = lambda name, content, lookup: {"type": name, "data": lookup[name](content)}

#EXTRACT = {}
#FORMAT = {}

class Pattern:
    
    def __init__(self, name:str="", pats:list=[]) -> None:
        """
        patterns is a list of patterns that correspond to the same
        markup. so we chose the first pattern from the list to represent
        the patterns
        """
        self.name = name
        left, right = pats[0]
        
        ## functions
        self.extract = lambda x: x[len(left):len(right)*(-1)]
        self.format = lambda x: f"{left}{x}{right}"
        
        ## regex patterns
        self.re_pattern = generate_pattern(name, pats)
        

class PatternManager:
    
    def __init__(self, cases:list=[]) -> None:
        self.EXTRACT = {}
        self.FORMAT = {}
        self.PATTERNS = []
        self.RE_INLINE_PATTERNS = self.generate_regex(cases)
        
    def create_pattern(self, name, pat):
        return Pattern(name, pat)
    
    def add_pattern(self, name, pats):
        pat = self.create_pattern(name, pats)
        self.EXTRACT[name] = pat.extract
        self.FORMAT[name] = pat.format
        self.PATTERNS.append(pat.re_pattern)
        
    def add_patterns(self, cases):
        for case in cases:
            pats, name = case
            self.add_pattern(name, pats)
        
    def generate_regex(self, cases):
        self.add_patterns(cases)
        print(join_patterns(self.PATTERNS))
        return re.compile(join_patterns(self.PATTERNS))
    
    
    def find_and_convert_inline(self, source:str="", bank:list=[]) -> Union[str, List]:
        """
        using our inline markup pattern, create a generator
        that will return non overlapping markup
        use this to split the text.
        return a list of converted blocks or the source string
        """
        pos_previous = (0,0)
        pos_current = (0,0)
        
        positions = [(0,0)]
        non_overlapping_content = []

        matches = self.create_inline_markup_iterator(source)

        for _ in matches:
            pos_previous = positions[-1]
            # last group returns the last group to match
            # which in our case is the only group to match
            name = _.lastgroup

            # get the current position of the match
            pos_current = _.span()

            # extract the text between the previous match and the current match
            text_between = get_text_between(pos_previous, pos_current, source)
            if len(text_between):
                # if its too small, let it go, it aint worth it
                new_between = create_text_object(text_between)
                non_overlapping_content.append(new_between)
                bank.append(new_between)

            # extract the text captured
            text_captured = get_text_captured(pos_current, source)
            new_captured = self.create_inline_markup_block(name, text_captured)
            non_overlapping_content.append(new_captured)
            bank.append(new_captured)

            # set the previous position to the current position
            positions.append(pos_current)
            #pos_previous = pos_current

        if len(non_overlapping_content):
            # make sure we only do this if there is content before
            text_after = get_text_after(pos_current, source)
            if len(text_after):
                # if its too small, let it go, it aint worth it
                new_after = create_text_object(text_after)
                non_overlapping_content.append(new_after)
                bank.append(new_after)

        if len(non_overlapping_content):
            return non_overlapping_content
        return source


    def convert_recursively(self, blocklist:list=[], level:int=1, bank:list=[]):
        """
        receive a list of blocks
        loop over the blocks until we are not converting nothing no more
        
        we are making the assumption that any blocks of type 'text' do not have
        any inline markup. the logic being that we are jumping from inline markup 
        chosing the next markup object that is both largest and soonest. 
        """
        for block in blocklist:
            if block["type"] != "text" and isinstance(block["data"], str):
                converted = self.find_and_convert_inline(block["data"], bank)
                if isinstance(converted, list) and len(converted):
                    block["data"] = converted
                    self.convert_recursively(block["data"], level+1, bank)
        return


    def convert(self, source:str="") -> list:
        mybank = []
        block_root = {"type": "root", "data": source}
        block_data_as_list = [block_root]
        self.convert_recursively(block_data_as_list, 1, mybank)

        #for _ in filter(lambda x: isinstance(x["data"], str), mybank):
        #    print(_)
        return block_root["data"]


    def revert(self, blocklist:list=[]) -> str:
        current_level = []
        for b in blocklist:
            if isinstance(b["data"], list):
                b["data"] = self.revert(b["data"])
            if isinstance(b["data"], str):
                if b["type"] != "text":
                    line = self.format_content(b)
                    current_level.append(line)
                else:
                    current_level.append(b["data"])
        return "".join(current_level)
    
    
    def create_inline_markup_iterator(self, source:str=""):
        return self.RE_INLINE_PATTERNS.finditer(source)
    
    def create_inline_markup_block(self, name:str="", content:str=""):
        return {"type": name, "data": self.extract_content(name, content)}

    def extract_content(self, name:str="", content:str=""):
        return self.EXTRACT[name](content)
    
    def format_content(self, block:dict={}):
        return self.FORMAT[block["type"]](block["data"])

MD = [
    """**Markdown Example** with _**Inline Markup**_.""",
    """This is a **bold** statement, and this is an _italicized_ one.""",
    """You can even combine them to make text _**both italic and bold**_.""",
    """If you need to reference a link, here's a [link to Markdown documentation](https://www.markdownguide.org).""",
    """This item has some inline markup like _italics_ and **bold** text.""",
    """Nested list item with a [link to a website](https://example.com) and some `inline code`.""",
    """Even deeper nesting: _Italicized_ **bold** list item with `code` inline.""",
    """Another item with **nested** inline **markup**.""",
    """This list item uses some `inline code` and ends with _**italicized and bold**_ text.""",
    """To write code, you can use backticks for `inline code`, like this.""",
]


MD = " ".join(MD)

pm = PatternManager(CASES)
converted = pm.convert(MD)


print(converted)
reverted = pm.revert(converted)
print(reverted)

if MD == reverted:
    print("correct")
else:
    print(repr(MD))
    print(repr(reverted))
print("done")

# %%
