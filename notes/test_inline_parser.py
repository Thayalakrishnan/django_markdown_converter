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
 

(?:``.+?``)|(?:__.+?__)|(?:\*\*.+?\*\*)|(?:~~.+?~~)|(?:--.+?--)|(?:==.+?==)|(?:\^\^.+?\^\^)|(?:`.+?`)|(?:\*.+?\*)|(?:\:.+?\:)|(?:~.+?~)|(?:\$.+?\$)|(?:_.+?_)
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

MD = 