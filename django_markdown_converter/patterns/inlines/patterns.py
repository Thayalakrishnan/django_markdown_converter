import re
from typing import Pattern, Callable
from django_markdown_converter.helpers.processors import convert_props, revert_props


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
#   - tag:str="", 
#   - pattern:tuple=(left, middle, right), 
#   - props:list=[], 
#   - revert_func:Callable=lambda x: x
# if we have a custom vue element, replace the tag with that element
CASES_LIST = [
    ("navlink", ("<navlink ", r'(?P<content>(?P<props>.*?)\>(?P<text>.*?))', "</navlink>"), ("props", "text"), lambda x: f"{revert_props(x.get('props', {}))}\>({x.get('text', '')}"),
    ("samp", ("``", r'(?P<content>.+?)', "``"), (), None),
    ("code", ("`", r'(?P<content>[^`]+?)', "`"), (), None),
    ("email", ("<", r'(?P<content>\S+@\S+)', ">"), (), None),
    ("rawlink", ("<", r'(?P<content>https\S+)', ">"), (), None),
    ("strong", ("**", R_CONTENT_NO_WSPACE, "**"), (), None),
    ("strong", ("__", R_CONTENT_NO_WSPACE, "__"), (), None),
    ("strong", ("**", r"(?P<content>.*?)", "**"), (), None),
    ("em", ("*", r"(?P<content>\*\*.*?\*\*)", "*"), (), None),
    ("strong", ("**", r"(?P<content>\*.*?\*)", "**"), (), None),
    ("strong", ("__", R_CONTENT, "__"), (), None),
    ("del", ("~~", R_CONTENT, "~~"), (), None),
    ("del", ("--", R_CONTENT, "--"), (), None),
    ("mark", ("==", R_CONTENT, "=="), (), None),
    ("emoji", (":", r'(?P<content>\S+)', ":"), (), None),
    ("em", ("_", R_CONTENT_NO_WSPACE, "_"), (), None),
    ("em", ("*", r"(?P<content>[^*]+?)", "*"), (), None),
    ("em", ("_", r"(?P<content>[^_]+?)", "_"), (), None),
    ("footnote", ("[^", r'(?P<content>\d+?)', "]"), (), None),
    ("link", ("[", R_CONTENT_LINK,")"), ("to", "title"), lambda x: f"{x.get('title', '')}]({x.get('to', '')}"),
    ("sup", ("^", r"(?P<content>[^\^]+?)", "^"), (), None),
    ("sub", ("~", r"(?P<content>[^~]+?)", "~"), (), None),
    ("math", ("$", R_CONTENT_NO_WSPACE, "$"), (), None),
]

class InlinePattern:
    """
    inline patterns case
    """
    __slots__ = ("left", "middle", "right", "pattern", "tag", "props", "hasAttrs", "revert_func")
    
    def __init__(self, pattern_object:tuple=()) -> None:
        self.tag = pattern_object[0]
        
        pattern = pattern_object[1]
        self.left = pattern[0]
        self.middle = pattern[1]
        self.right = pattern[2]
        self.pattern = re.compile(R_BEFORE(self.left) + self.middle + R_AFTER(self.right))
        
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
    

class InlinePatternManager:
    """
    inline patterns case
    """
    __slots__ = ("patterns", "pattern_lookup")

    def __init__(self, cases:list=[]) -> None:
        self.patterns = []
        self.pattern_lookup = {}
        self.add_patterns(cases=cases)

    @staticmethod
    def construct_pattern(left:str, middle:InlinePattern, right:str):
        return re.compile(R_BEFORE(left) + middle + R_AFTER(right))

    def add_pattern(self, case:list):
        new_pattern = InlinePattern(case)
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


CASES = InlinePatternManager(CASES_LIST)

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
