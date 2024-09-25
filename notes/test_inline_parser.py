import re
from typing import Union, List

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
"""
(?<=\b).+?(?=\b)
(?P<o>\W|\W\W).+?(?P=o)
 (?P<o>(?:(?:`)|(?:``)|(?:\*)|(?:\*\*)|(?:~~)|(?:\:)|(?:--)|(?:==)|(?:\^\^)|(?:~)|(?:\$)|(?:_)|(?:__))).+?(?P=o)


(?:``.+?``)|
(?:__.+?__)|
(?:\*\*.+?\*\*)|
(?:~~.+?~~)|
(?:--.+?--)|
(?:==.+?==)|
(?:\^\^.+?\^\^)|
(?:`.+?`)|
(?:\*.+?\*)|
(?:\:.+?\:)|
(?:~.+?~)|
(?:\$.+?\$)|
(?:_.+?_)
"""
INLINE_PATTERN_RAW = r'(?P<block>^(?:```.*?```.*?)|(?:.*?))(?:^\{(?P<props>.*?)\} *?$\n)?^\n'
# r"""(?P<open>(?:\`)|(?:\_\_)|(?:\_\_)|(?:\_\_)|(?:\_\_))  # the integral part
INLINE_PATTERN = re.compile(r"(?P<open>(?:\`)|(?:\_\_)).*?(?P=open)", re.MULTILINE | re.DOTALL)
INLINE_PATTERN = re.compile(r"(?P<o>(?:\`)|(?:\_\_)).*?(?P=o)", re.MULTILINE | re.DOTALL)
INLINE_PATTERN = re.compile(
    r"""
    (?P<o>
        (?:\`)|
        (?:\`\`)|
        (?:\*)|
        (?:\*\*)|
        (?:\~\~)|
        (?:\:)|
        (?:\-\-)|
        (?:\=\=)|
        (?:\^\^)|
        (?:\~)|
        (?:\$)|
        (?:\_))
        (?:\_\_))
    .*?
    (?P=o)"""
    , re.MULTILINE | re.DOTALL | re.VERBOSE)

#INLINE_PATTERN = re.compile(INLINE_PATTERN_RAW, re.MULTILINE | re.DOTALL | re.VERBOSE)

INLINE_PATTERN_RAW = r'(?:``.+?``)|(?:__.+?__)|(?:\*\*.+?\*\*)|(?:~~.+?~~)|(?:--.+?--)|(?:==.+?==)|(?:\^\^.+?\^\^)|(?:`.+?`)|(?:\*.+?\*)|(?:\:.+?\:)|(?:~.+?~)|(?:\$.+?\$)|(?:_.+?_)'
INLINE_PATTERN = re.compile(INLINE_PATTERN_RAW)

MD = ""




# %%



import re

pattern1 = re.compile(r'(?:\_\_)')
pattern2 = re.compile(r'(?:__)')
pattern3 = re.compile(re.escape(r'(?:__)'))

#print(pattern1.pattern)
#print(pattern2.pattern)
#print(pattern3.pattern)

pattern1 = f'(?:**)'
pattern2 = r'(?:**)'
pattern3 = f'(?:\*\*)'
pattern4 = r'(?:\*\*)'
pattern5 = re.escape(pattern1)
pattern6 = re.escape(pattern2)
pattern7 = re.escape(pattern3)
pattern8 = re.escape(pattern4)
pattern9 = r'(?:' + re.escape("**") + r')'
pattern10 = f'(?:{re.escape("**")})'

print(repr(pattern1)) #  '(?:**)' | f string
print(repr(pattern2)) #  '(?:**)' | raw string
print(repr(pattern3)) #  '(?:\\*\\*)' | f string with escaped characters
print(repr(pattern4)) #  '(?:\\*\\*)' | raw string with escaped characters
print(repr(pattern5)) #  '\\(\\?:\\*\\*\\)' | re.escaped f string
print(repr(pattern6)) #  '\\(\\?:\\*\\*\\)' | re.escaped raw string
print(repr(pattern7)) #  '\\(\\?:\\\\\\*\\\\\\*\\)' | re.escaped raw string
print(repr(pattern8)) #  '\\(\\?:\\\\\\*\\\\\\*\\)' | re.escaped raw string
print(repr(pattern9)) #  '(?:\\*\\*)' |
print(repr(pattern10)) # '(?:\\*\\*)' |

print(pattern1) # (?:**) | f string
print(pattern2) # (?:**) | raw string
print(pattern3) # (?:\*\*) | f string with escaped characters
print(pattern4) # (?:\*\*) | raw string with escaped characters
print(pattern5) # \(\?:\*\*\) | re.escaped f string
print(pattern6) # \(\?:\*\*\) | re.escaped raw string
print(pattern7) # \(\?:\\\*\\\*\) | re.escaped raw string
print(pattern8) # \(\?:\\\*\\\*\) | re.escaped raw string
print(pattern9) # (?:\*\*) |
print(pattern10) # (?:\*\*) |


## repr returns the canonical representation of the string
## it escapes characters so that they can be printed on stdout

"""
'end': 
'endpos': 
'expand': 
'group': 
'groupdict': 
'groups': 
'lastgroup': 
'lastindex': 
'pos': 
're': 
'regs': 
'span': 
'start': 
'string': full input string
"""
#%%
import re
from typing import Union, List

CASES = [
    ## symettrical
    [ ("`", "`"), "code", True, "code"],
    [ ("__", "__"), "strong", True, "strong"],
    [ ("**", "**"), "strong2", True, "strong"],
    [ ("*", "*"), "em", True, "em"],
    [ ("_", "_"), "em2", True, "em"],
    [ ("~~", "~~"), "del", True, "del"],
    [ ("--", "--"), "del2", True, "del"],
    [ ("==", "=="), "mark", True, "mark"],
    [ ("``", "``"), "samp", True, "samp"],
    [ (":", ":"), "emoji", True, "emoji"],
    [ ("^", "^"), "sup", True, "sup"],
    [ ("~", "~"), "sub", True, "sub"],
    [ ("$", "$"), "math", True, "math"],
    ## non symettrical
    [ ("<navlink ", "</navlink>"), "navlink", False, "navlink"],
    [ ("<", ">"), "rawlink", False, "rawlink"],
    [ ("[^", "]"), "footnote", False, "footnote"],
    [ ("[", ")"), "link", False, "link"],
    #[ (" ", " "), "text", True, "text"],
]

def lambda_extractor(len_start:int=0, len_stop:int=0):
    return lambda x: x[len_start:len_stop*(-1)]

compilespatterns = []
symettrical_pattern = lambda x, l: f"(?P<{l}>(?:{x}).+?(?:{x}))"
non_symettrical_pattern = lambda x,y,l: f"(?P<{l}>(?:{x}).+?(?:{y}))"

EXTRACT = {}

for case in CASES:
    pattern, key, symmetrical, name = case
    if not symmetrical:
        cpattern = non_symettrical_pattern(re.escape(pattern[0]), re.escape(pattern[1]), key)
    else:
        cpattern = non_symettrical_pattern(re.escape(pattern[0]), re.escape(pattern[1]), key)
        #cpattern = symettrical_pattern(re.escape(pattern[0]), key)
    EXTRACT[key] = lambda_extractor(len(pattern[0]), len(pattern[1]))
    compilespatterns.append(cpattern)

# no flags
INLINE_MARKUP_PATTERN_RAW = "|".join(compilespatterns)
print(INLINE_MARKUP_PATTERN_RAW)

INLINE_MARKUP_PATTERN = re.compile(INLINE_MARKUP_PATTERN_RAW)

MD = [
    """**Markdown Example** with _**Inline Markup**_.""",
    #"""This is a **bold** statement, and this is an _italicized_ one.""",
    #"""You can even combine them to make text _**both italic and bold**_.""",
    #"""If you need to reference a link, here's a [link to Markdown documentation](https://www.markdownguide.org).""",
    #"""This item has some inline markup like _italics_ and **bold** text.""",
    #"""Nested list item with a [link to a website](https://example.com) and some `inline code`.""",
    #"""Even deeper nesting: _Italicized_ **bold** list item with `code` inline.""",
    #"""Another item with **nested** inline **markup**.""",
    #"""This list item uses some `inline code` and ends with _**italicized and bold**_ text.""",
    #"""To write code, you can use backticks for `inline code`, like this.""",
]
MD = " ".join(MD)

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

# %%

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
# %%
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

mybank = []
block_data_as_list = [{"type": "root", "data": MD}]
loop_over_data_and_conver_inline(block_data_as_list, 1, mybank)

#print(block_data_as_list)

for _ in filter(lambda x: isinstance(x["data"], str), mybank):
    print(_)
    
#for _ in mybank:
#    print(_)
   
print("done")
# %%
