import re
from typing import Pattern

# everything inbetween
R_CONTENT = r'(?P<content>.*?)'
R_BEFORE = lambda pat: f'(?P<before>.*?)(?P<left>{re.escape(pat)})'
R_AFTER = lambda pat: f'(?P<right>{re.escape(pat)})(?P<after>.*)'

R_CONTENT_ONE_OR_MORE = r'(?P<content>.+?)'

# everything inbetween except whitespace
R_CONTENT_NO_WSPACE = r'(?P<content>\S+)'

R_CONTENT_RAWLINK = r'(?P<content>https\S+)'
R_CONTENT_EMOJI = r'(?P<content>\S+)'
R_CONTENT_FOOTNOTE = r'(?P<content>\d+?)'

# inline image
R_CONTENT_INLINE_IMAGE = r'(?P<content>(?P<alt>.*?)\]\((?P<src>.*?))'
R_CONTENT_INLINE_IMAGE = r'(?P<content>(?P<props>.*?)\]\((?P<src>.*?))'

# inline LINK
R_CONTENT_LINK = r'(?P<content>(?P<title>.*?)\]\((?P<to>.*?))'

# inline LINK
R_EMAIL = r'(?P<content>\S+@\S+)'





# [pattern, tag, type, props]
# if we have a custom vue element, replace the tag with that element
CASES_LIST = [
    [ ("<navlink ", r'(?P<content>(?P<props>.*?)\>(?P<text>.*?))', "</navlink>"), "navlink", ["props", "text"] ],
    [ ("`", r'(?P<content>.*?)', "`"), "code", [] ],
    #[ ("`", r'(?P<content>[^`]+?)', "`"), [] ],
    [ ("<", R_EMAIL, ">"), "email", [] ],
    [ ("<", R_CONTENT_RAWLINK, ">"),  "rawlink", [] ],
    [ ("**", R_CONTENT_NO_WSPACE, "**"), "strong", [] ],
    [ ("__", R_CONTENT_NO_WSPACE, "__"), "strong", [] ],
    [ ("**", r"(?P<content>.*?)", "**"), "strong", [] ],
    [ ("*", r"(?P<content>\*\*.*?\*\*)", "*"), "em", [] ],
    [ ("**", r"(?P<content>\*.*?\*)", "**"), "strong", [] ],
    [ ("__", R_CONTENT, "__"), "strong", [] ],
    [ ("~~", R_CONTENT, "~~"), "del", [] ],
    [ ("--", R_CONTENT, "--"), "del", [] ],
    [ ("==", R_CONTENT, "=="), "mark", [] ],
    [ ("``", R_CONTENT, "``"), "samp", [] ],
    [ (":", R_CONTENT_EMOJI, ":"), "emoji", [] ],
    [ ("_", R_CONTENT_NO_WSPACE, "_"),  "em", [] ],
    [ ("*", r"(?P<content>[^*]+?)", "*"),  "em", [] ],
    [ ("_", r"(?P<content>[^_]+?)", "_"),  "em", [] ],
    #[ ("![", R_CONTENT_INLINE_IMAGE, ")"), "image", ["props", "src"] ],
    [ ("[^", R_CONTENT_FOOTNOTE, "]"), "footnote", [] ],
    [ ("[", R_CONTENT_LINK,")"),  "link", ["to", "title"] ],
    [ ("^", R_CONTENT_NO_WSPACE, "^"), "sup", [] ],
    [ ("~", r"(?P<content>[^~]+?)", "~"), "sub", [] ],
    [ ("$", R_CONTENT_NO_WSPACE, "$"),  "math", [] ],
]


class Pattern:
    """
    inline patterns case
    """
    __slots__ = ("pattern", "tag", "props")

    def __init__(self, pattern:Pattern, tag:str, props:list) -> None:
        self.pattern = pattern
        self.tag = tag
        self.props = props

class PatternManager:
    """
    inline patterns case
    """
    __slots__ = ("patterns",)

    def __init__(self, cases:list=[]) -> None:
        self.patterns = []
        for case in cases:
            self.add_pattern(case)

    @staticmethod
    def construct_pattern(left:str, middle:Pattern, right:str):
        return re.compile(R_BEFORE(left) + middle + R_AFTER(right))

    def add_pattern(self, case:list):
        pattern = self.construct_pattern(*case[0])
        self.patterns.append(Pattern(pattern, case[1], case[2]))


def build_element_pattern(left:str, middle:Pattern, right:str):
    return re.compile(R_BEFORE(left) + middle + R_AFTER(right))

def build_patterns(cases_list:list) -> list:
    """using the cases list, build an array of inline patterns to match against"""
    cases = []
    for case in cases_list:
        pattern = build_element_pattern(*case[0])
        cases.append(Pattern(pattern, case[1], case[2]))
    return cases


def find_boundary(cases:list=[], line:str=""):
    """
    for the given line, loop over each boundary case and check which one
    is the closest
    we should also ensure the size of the match is greater for
    two competing matches
    """

    cur_match = None
    cur_boundary = False
    cur_start = len(line)

    for boundary in cases:
        match = boundary.pattern.search(line)
        if match:
            new_start = match.start("content")
            """
            situation 1: nested tags
            situation 2: tags before other tags
            """
            if (new_start < cur_start):
                cur_match = match
                cur_boundary = boundary
                cur_start = new_start

    return (cur_match, cur_boundary)


def convert_text(cases:list=[], line:str="", level:list=[]):
    """loop over the lines for testing"""

    match, boundary = find_boundary(cases, line)

    """if we have matched a valid boundary, extract it, if not return"""
    if boundary:
        before, middle, after = match.group("before"), match.group("content"), match.group("after")
        if len(before):
            level.append({"tag": "text", "data": before})
        if len(middle):
            if boundary.props:
                props = {}
                for prop in boundary.props:
                    if prop == "props":
                        # if the props is props, then we have a series of key value pairs
                        # we should be able to split them into their individual properties
                        rawprop = match.group(prop)
                        if "=" in rawprop:
                            props = rawprop.strip().split(" ")
                            for attr in props:
                                k,v = attr.split("=")
                                props[k] = v.strip("'\"")
                        else:
                            props["data"] = rawprop
                    else:
                        props[prop] = match.group(prop)
                #level.append({"tag": boundary.tag, "props": props, "data": middle})
                level.append({"tag": boundary.tag, "data": props})
            else:
                level.append({"tag": boundary.tag, "data": middle})
        if len(after):
            return convert_text(cases, after, level)
    else:
        if len(level):
            if len(line):
                level.append({"tag": "text", "data": line})
                #level.append(line)
            else:
                return line
            return level
        #print(f"tiny line: {line}")
        return line
    return level


CASES = build_patterns(CASES_LIST)

def inline_block_parser(block:dict={}, counter=0) -> dict:
    if isinstance(block["data"], dict):
        return
    
    block["data"] = convert_text(CASES, block["data"], [])
    counter+=1

    if isinstance(block["data"], list) and len(block["data"]):
        for _ in block["data"]:
            inline_block_parser(_, counter)



def inline_parser(lines:str="") -> list:
    pblock = {"data": lines}
    inline_block_parser(pblock)
    
    
    return pblock["data"]


