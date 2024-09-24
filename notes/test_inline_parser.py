import re
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


#%%
CASES = [
    ## symettrical
    [ ("`", "`"), "code", True ],
    [ ("__", "__"), "strong", True ],
    [ ("**", "**"), "strong2", True ],
    [ ("*", "*"),  "em", True ],
    [ ("_", "_"),  "em2", True ],
    [ ("~~", "~~"), "del", True ],
    [ ("--", "--"), "del2", True ],
    [ ("==", "=="), "mark", True ],
    [ ("``", "``"), "samp", True ],
    [ (":", ":"), "emoji", True ],
    [ ("^", "^"), "sup", True ],
    [ ("~", "~"), "sub", True ],
    [ ("$", "$"),  "math", True ],
    ## non symettrical
    [ ("<navlink ", "</navlink>"), "navlink", False ],
    [ ("<", ">"),  "rawlink", False ],
    [ ("[^", "]"), "footnote", False ],
    [ ("[", ")"),  "link", False ],
]

compilespatterns = []
symettrical_pattern = lambda x, l: f"(?P<{l}>({x})(.+?)({x}))"
non_symettrical_pattern = lambda x,y,l: f"(?P<{l}>({x})(.+?)({y}))"

symettrical_pattern = lambda x, l: f"(?P<{l}>(?<={x})(.+?)(?={x}))"
non_symettrical_pattern = lambda x,y,l: f"(?P<{l}>(?<={x})(.+?)(?={y}))"

symettrical_pattern = lambda x, l: f"(?P<{l}>(?:{x}).+?(?:{x}))"
non_symettrical_pattern = lambda x,y,l: f"(?P<{l}>(?:{x}).+?(?:{y}))"


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

for case in CASES:
    pattern, key, symmetrical = case

    if not symmetrical:
        cpattern = non_symettrical_pattern(re.escape(pattern[0]), re.escape(pattern[1]), key)
    else:
        cpattern = symettrical_pattern(re.escape(pattern[0]), key)
    compilespatterns.append(cpattern)
    print(cpattern)

print("|".join(compilespatterns))
pat = re.compile("|".join(compilespatterns))

#%%
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

matches = pat.finditer(" ".join(MD))

for _ in matches:
    # last group returns the last group to match
    # which in our case is the only group to match
    group_key = _.lastgroup 
    group = _.group(group_key)
    print(group)
    print(_.span())
    
# %%
