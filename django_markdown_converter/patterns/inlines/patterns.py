import re
from typing import Pattern, Callable
from django_markdown_converter.helpers.processors import convert_props


# everything inbetween
R_BEFORE = lambda pat: f'(?P<before>.*?)(?P<left>{re.escape(pat)})'
R_AFTER = lambda pat: f'(?P<right>{re.escape(pat)})(?P<after>.*)'

# everything inbetween
R_CONTENT = r'(?P<content>.*?)'
# everything inbetween except whitespace
R_CONTENT_NO_WSPACE = r'(?P<content>\S+)'

# inline LINK
R_CONTENT_LINK = r'(?P<content>(?P<title>[^\]]*?)\]\((?P<to>[^\)]*?))'

## inline reversion functions
INLINE_TAG_LOOKUP = {
    ## symetrical
    "text": lambda x: f"{x}",
    "email": lambda x: f"<{x}>",
    "code": lambda x: f"`{x}`",
    "strong": lambda x: f"**{x}**",
    "em": lambda x: f"_{x}_",
    "del": lambda x: f"--{x}--",
    "mark": lambda x: f"=={x}==",
    "samp": lambda x: f"``{x}``",
    "emoji": lambda x: f":{x}:",
    "sup": lambda x: f"^{x}^",
    "sub": lambda x: f"~{x}~",
    "math": lambda x: f"${x}$",
    ## not
    "footnote": lambda x: f"[^{x}]",
    "link": lambda x: f"{x.get('title', '')}]({x.get('to', '')}",
}

# [pattern, tag, type, props]
#   - pattern:tuple=(left, middle, right), 
#   - tag:str="", 
#   - props:list=[], 
#   - revert_func:Callable=lambda x: x
# if we have a custom vue element, replace the tag with that element
CASES_LIST = [
    (("<navlink ", r'(?P<content>(?P<props>.*?)\>(?P<text>.*?))', "</navlink>"), "navlink", ("props", "text"), lambda x: f"{revert_props(x.get('props', {}))}\>({x.get('text', '')}"),
    (("``", r'(?P<content>.+?)', "``"), "samp", (), None),
    (("`", r'(?P<content>[^`]+?)', "`"), "code", (), None),
    (("<", r'(?P<content>\S+@\S+)', ">"), "email", (), None),
    (("<", r'(?P<content>https\S+)', ">"),  "rawlink", (), None),
    (("**", R_CONTENT_NO_WSPACE, "**"), "strong", (), None),
    (("__", R_CONTENT_NO_WSPACE, "__"), "strong", (), None),
    (("**", r"(?P<content>.*?)", "**"), "strong", (), None),
    (("*", r"(?P<content>\*\*.*?\*\*)", "*"), "em", (), None),
    (("**", r"(?P<content>\*.*?\*)", "**"), "strong", (), None),
    (("__", R_CONTENT, "__"), "strong", (), None),
    (("~~", R_CONTENT, "~~"), "del", (), None),
    (("--", R_CONTENT, "--"), "del", (), None),
    (("==", R_CONTENT, "=="), "mark", (), None),
    ((":", r'(?P<content>\S+)', ":"), "emoji", (), None),
    (("_", R_CONTENT_NO_WSPACE, "_"),  "em", (), None),
    (("*", r"(?P<content>[^*]+?)", "*"),  "em", (), None),
    (("_", r"(?P<content>[^_]+?)", "_"),  "em", (), None),
    (("[^", r'(?P<content>\d+?)', "]"), "footnote", (), None),
    (("[", R_CONTENT_LINK,")"),  "link", ("to", "title"), lambda x: f"{x.get('title', '')}]({x.get('to', '')}"),
    (("^", r"(?P<content>[^\^]+?)", "^"), "sup", (), None),
    (("~", r"(?P<content>[^~]+?)", "~"), "sub", (), None),
    (("$", R_CONTENT_NO_WSPACE, "$"),  "math", (), None),
]

class Pattern:
    """
    inline patterns case
    """
    __slots__ = ("left", "middle", "right", "pattern", "tag", "props", "hasAttrs", "revert_func")
    
    def __init__(self, pattern_object:tuple=()) -> None:
        pattern = pattern_object[0]
        self.left = pattern[0]
        self.middle = pattern[1]
        self.right = pattern[2]
        
        self.pattern = re.compile(R_BEFORE(self.left) + self.middle + R_AFTER(self.right))
        
        self.tag = pattern_object[1]
        self.props = pattern_object[2]
        self.hasAttrs = "attrs" in self.props
        self.revert_func = pattern_object[3]
    
    def __repr__(self) -> str:
        return self.tag
    
    def __str__(self) -> str:
        return self.tag
    
    def getData(self, string:str=""):
        return string
    
    def convert(self, string:str=""):
        return {"tag": self.tag, "data": self.getData(string)}
    
    def revert(self, block:dict={}):
        data = block.get("data", "")
        if self.revert_func:
            data = self.revert_func(data)
        return f"{self.left}{data}{self.right}"
    

class PatternManager:
    """
    inline patterns case
    """
    __slots__ = ("patterns", "pattern_lookup")

    def __init__(self, cases:list=[]) -> None:
        self.patterns = []
        self.pattern_lookup = {}
        self.add_patterns(cases=cases)

    @staticmethod
    def construct_pattern(left:str, middle:Pattern, right:str):
        return re.compile(R_BEFORE(left) + middle + R_AFTER(right))

    def add_pattern(self, case:list):
        new_pattern = Pattern(case)
        self.patterns.append(new_pattern)
        self.pattern_lookup.update({new_pattern.tag: new_pattern})
    
    def add_patterns(self, cases:list=[]):
        for case in cases:
            self.add_pattern(case)

def process_inline_props(rawprops:str=""):
    if "=" in rawprops:
        processed_props = convert_props(rawprops)
        if processed_props:
            return processed_props
    return {"data": rawprops}


CASES = PatternManager(CASES_LIST)

INLINE_TAG_KEYS = {
    ## symetrical
    "text": None,
    "email": None,
    "code": None,
    "strong": None,
    "em": None,
    "del": None,
    "mark": None,
    "samp": None,
    "emoji": None,
    "sup": None,
    "sub": None,
    "math": None,
    ## not
    "footnote": None,
    "link": {"to": "", "title": ""},
}
