#%%
import re
from typing import Union, List


"""
(?<=\b).+?(?=\b)
(?P<o>\W|\W\W).+?(?P=o)

(?P<code>(?:`).+?(?:`))|
(?P<strong>(?:__).+?(?:__))|
(?P<strong2>(?:\*\*).+?(?:\*\*))|
(?P<em>(?:\*).+?(?:\*))|
(?P<em2>(?:_).+?(?:_))|
(?P<del>(?:\~\~).+?(?:\~\~))|
(?P<del2>(?:\-\-).+?(?:\-\-))|
(?P<mark>(?:==).+?(?:==))|
(?P<samp>(?:``).+?(?:``))|
(?P<emoji>(?::).+?(?::))|
(?P<sup>(?:\^).+?(?:\^))|
(?P<sub>(?:\~).+?(?:\~))|
(?P<math>(?:\$).+?(?:\$))|
(?P<navlink>(?:<navlink\ ).+?(?:</navlink>))|
(?P<rawlink>(?:<).+?(?:>))|
(?P<footnote>(?:\[\^).+?(?:\]))|
(?P<link>(?:\[).+?(?:\)))



(?P<code>(?:`).+?(?:`))|
(?P<strong>(__.+?__)|(\*\*.+?\*\*))|
(?P<em>(\*.+?\*)|(_.+?_))|
(?P<del>(\~\~.+?\~\~)|(\-\-.+?\-\-))|
(?P<mark>(?:==).+?(?:==))|
(?P<samp>(?:``).+?(?:``))|
(?P<emoji>(?::).+?(?::))|
(?P<sup>(?:\^).+?(?:\^))|
(?P<sub>(?:\~).+?(?:\~))|
(?P<math>(?:\$).+?(?:\$))|
(?P<navlink>(?:<navlink\ ).+?(?:</navlink>))|
(?P<rawlink>(?:<).+?(?:>))|
(?P<footnote>(?:\[\^).+?(?:\]))|
(?P<link>(?:\[).+?(?:\)))
"""


"""
pattern
name
symmetrical?
"""
CASES_LIST = [
    ## symettrical
    [ ("`", "`"), "code", True ],
    [ ("__", "__"), "strong", True ],
    [ ("**", "**"), "strong", True ],
    [ ("*", "*"),  "em", True ],
    [ ("_", "_"),  "em", True ],
    [ ("~~", "~~"), "del", True ],
    [ ("--", "--"), "del", True ],
    [ ("==", "=="), "mark", True ],
    [ ("``", "``"), "samp", True ],
    [ (":", ":"), "emoji", True ],
    [ ("^", "^"), "sup", True ],
    [ ("~", "~"), "sub", True ],
    [ ("$", "$"),  "math", True ],

    ## non symettrical
    [ ("<navlink ", "</navlink>"), "navlink", False ],
    [ ("<", ">"), "email", False ],
    [ ("<", ">"),  "rawlink", False ],
    [ ("[^", "]"), "footnote", False ],
    [ ("[", ")"),  "link", False ],
]

INLINE_MARKUP_PATTERN = re.compile(
    r"""
    (?P<code>(?:`).+?(?:`))|
    (?P<strong>(?P<substrong>(?:\*\*)|(?:__)).+?(?P=substrong))|
    (?P<em>(?P<subem>(?:\*)|(?:_)).+?(?P=subem))|
    (?P<del>(?P<subdel>(?:\~\~)|(?:\-\-)).+?(?P=subdel))|
    (?P<mark>(?:==).+?(?:==))|
    (?P<samp>(?:``).+?(?:``))|
    (?P<emoji>(?::).+?(?::))|
    (?P<sup>(?:\^).+?(?:\^))|
    (?P<sub>(?:\~).+?(?:\~))|
    (?P<math>(?:\$).+?(?:\$))|
    (?P<navlink>(?:<navlink\ ).+?(?:</navlink>))|
    (?P<rawlink>(?:<).+?(?:>))|
    (?P<footnote>(?:\[\^).+?(?:\]))|
    (?P<link>(?:\[).+?(?:\)))
    """
    , re.VERBOSE)

INLINE_MARKUP_PATTERN = re.compile(r"""
(?P<code>(?:`).+?(?:`))|
(?P<strong>(__.+?__)|(\*\*.+?\*\*))|
(?P<em>(\*.+?\*)|(_.+?_))|
(?P<del>(\~\~.+?\~\~)|(\-\-.+?\-\-))|
(?P<mark>(?:==).+?(?:==))|
(?P<samp>(?:``).+?(?:``))|
(?P<emoji>(?::).+?(?::))|
(?P<sup>(?:\^).+?(?:\^))|
(?P<sub>(?:\~).+?(?:\~))|
(?P<math>(?:\$).+?(?:\$))|
(?P<navlink>(?:<navlink\ ).+?(?:</navlink>))|
(?P<rawlink>(?:<).+?(?:>))|
(?P<footnote>(?:\[\^).+?(?:\]))|
(?P<link>(?:\[).+?(?:\)))""", re.VERBOSE)


#INLINE_MARKUP_PATTERN = re.compile(r'(?P<code>(?:`).+?(?:`))|(?P<strong>(__.+?__)|(\*\*.+?\*\*)|(?P<em>(\*.+?\*)|(_.+?_)|(?P<del>(\~\~.+?\~\~)|(\-\-.+?\-\-)|(?P<mark>(?:==).+?(?:==))|(?P<samp>(?:``).+?(?:``))|(?P<emoji>(?::).+?(?::))|(?P<sup>(?:\^).+?(?:\^))|(?P<sub>(?:\~).+?(?:\~))|(?P<math>(?:\$).+?(?:\$))|(?P<navlink>(?:<navlink\ ).+?(?:</navlink>))|(?P<rawlink>(?:<).+?(?:>))|(?P<footnote>(?:\[\^).+?(?:\]))|(?P<link>(?:\[).+?(?:\)))')

#INLINE_PATTERN_RAW = r'(?:``.+?``)|(?:__.+?__)|(?:\*\*.+?\*\*)|(?:~~.+?~~)|(?:--.+?--)|(?:==.+?==)|(?:\^\^.+?\^\^)|(?:`.+?`)|(?:\*.+?\*)|(?:\:.+?\:)|(?:~.+?~)|(?:\$.+?\$)|(?:_.+?_)'
#INLINE_PATTERN = re.compile(INLINE_PATTERN_RAW)

CASES = [
    ## symettrical
    [ ("`", "`"), "code", False, "code"],
    [ [("**", "**"), ("__", "__")], "strong", True, "strong"],
    [ [("*", "*"), ("_", "_")], "em", True, "em"],
    [ [("~~", "~~"), ("--", "--")], "del", True, "del"],
    [ ("==", "=="), "mark", False, "mark"],
    [ ("``", "``"), "samp", False, "samp"],
    [ (":", ":"), "emoji", False, "emoji"],
    [ ("^", "^"), "sup", False, "sup"],
    [ ("~", "~"), "sub", False, "sub"],
    [ ("$", "$"), "math", False, "math"],
    ## non symettrical
    [ ("<navlink ", "</navlink>"), "navlink", False, "navlink"],
    [ ("<", ">"), "rawlink", False, "rawlink"],
    [ ("[^", "]"), "footnote", False, "footnote"],
    [ ("[", ")"), "link", False, "link"],
    #[ (" ", " "), "text", True, "text"],
]

def lambda_extractor(len_start:int=0, len_stop:int=0):
    return lambda x: x[len_start:len_stop*(-1)]

def lambda_formatter(start:str="", stop:str=""):
    return lambda x: f"{start}{x}{stop}"


#def multi_pattern(patterns:list=[]):
#    for pat in patterns:
#        f"(?:{re.escape(pat[0])})"
#    
#    f"(?P<strong>(?P<substrong>(?:\*\*)|(?:__)).+?(?P=substrong))"
#    return lambda x: f"{start}{x}{stop}"

compilespatterns = []
symettrical_pattern = lambda x, l: f"(?P<{l}>(?:{x}).+?(?:{x}))"
non_symettrical_pattern = lambda x,y,l: f"(?P<{l}>(?:{x}).+?(?:{y}))"

EXTRACT = {}
FORMAT = {}

for case in CASES:
    
    pattern, key, multi, name = case
    
    if isinstance(pattern, list):
        # multpattern
        firstpattern = pattern[0]
        cpattern = non_symettrical_pattern(re.escape(firstpattern[0]), re.escape(firstpattern[1]), key)
        EXTRACT[key] = lambda_extractor(len(firstpattern[0]), len(firstpattern[1]))
        FORMAT[key] = lambda_formatter(firstpattern[0], firstpattern[1])
    else:
        cpattern = non_symettrical_pattern(re.escape(pattern[0]), re.escape(pattern[1]), key)
        EXTRACT[key] = lambda_extractor(len(pattern[0]), len(pattern[1]))
        FORMAT[key] = lambda_formatter(pattern[0], pattern[1])
    
    compilespatterns.append(cpattern)

# no flags
#INLINE_MARKUP_PATTERN_RAW = "|".join(compilespatterns)
#INLINE_MARKUP_PATTERN = re.compile(INLINE_MARKUP_PATTERN_RAW)

def extract_string(content:str="", pos:tuple=()):
    b, a = pos
    before, middle, after = content[0:b], content[b:a], content[a:]
    return before, middle, after

def get_text_captured(cur:tuple=(), content:str="") -> str:
    return content[cur[0]:cur[1]]

def get_text_between(pre:tuple=(), cur:tuple=(), content:str="") -> str:
    return content[pre[1]:cur[0]]

def get_text_after(cur:tuple=(), content:str="") -> str:
    return content[cur[1]::]


def create_text_object(content):
    return {
        "type": "text", 
        "data": content
    }
    
def create_markup_object(pattern_key, content):
    formatted_content = EXTRACT[pattern_key](content)
    return {
        "type": pattern_key, 
        "data": formatted_content
    }

def find_and_convert_inline(source:str="", bank:list=[]) -> Union[str, List]:
    """
    using our inline markup pattern, create a generator 
    that will return non overlapping markup
    use this to split the text. 
    return a list of converted blocks or the source string
    """
    pos_previous = (0,0)
    pos_current = (0,0)
    non_overlapping_content = []

    matches = INLINE_MARKUP_PATTERN.finditer(source)
    
    for _ in matches:
        # last group returns the last group to match
        # which in our case is the only group to match
        group_key = _.lastgroup
        
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
        new_captured = create_markup_object(group_key, text_captured)
        non_overlapping_content.append(new_captured)
        bank.append(new_captured)
        
        # set the previous position to the current position
        pos_previous = pos_current
    
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


def loop_over_data_and_conver_inline(blocklist:list=[], level:int=1, bank:list=[]):
    """
    receive a list of blocks
    loop over the blocks until we are not converting nothing no more
    """
    for block in blocklist:
        if block["type"] != "text" and isinstance(block["data"], str):
            converted = find_and_convert_inline(block["data"], bank)
            if isinstance(converted, list) and len(converted):
                block["data"] = converted
                loop_over_data_and_conver_inline(block["data"], level+1, bank)
    return

    
def convert(source:str="") -> list:
    mybank = []
    block_root = {"type": "root", "data": source}
    block_data_as_list = [block_root]
    loop_over_data_and_conver_inline(block_data_as_list, 1, mybank)

    #for _ in filter(lambda x: isinstance(x["data"], str), mybank):
    #    print(_)
    return block_root["data"]


def revert(blocklist:list=[]) -> str:
    current_level = []
    for b in blocklist:
        if isinstance(b["data"], list):
            b["data"] = revert(b["data"])
        if isinstance(b["data"], str):
            if b["type"] != "text":
                line = FORMAT[b["type"]](b["data"])
                current_level.append(line)
            else:
                current_level.append(b["data"])
    return "".join(current_level)


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

converted = convert(MD)
print(converted)
reverted = revert(converted)
print(reverted)

print("done")

# %%
