import re

from django_markdown_converter.helpers.processors import process_props


"""

captureprocess: 
- block is capture, funciton is called to process the captured content, which is the data
headerbody: 
- block heas a header and a body which both contribute to the final block
- header and body both need to be processed
- some of the header bodies have a header and simply a body that needs to be dedented/indented
    - capture, header, dedent
oneshot
- everything is done using the initial pattern
findall
- the given pattern selects multiple rows for this pattern, as they are normally lists
- the items then need to be 

[type, pattern, flags, process type, has Nested, has Inline Markup],

0 | type
1 | pattern
2 | flags
3 | process type
4 | has Nested
5 | has Inline Markup
6 | props

captureprocess
headerbody
oneshot
findall

"""


class Patties:
    
    def __init__(self, pattern_object:list=[], *args, **kwargs) -> None:
        self.blocktype = pattern_object[0]
        self.pattern = re.compile(pattern_object[1], pattern_object[2])
        self.process = pattern_object[3]
        self.hasNested = pattern_object[4]
        self.hasInline = pattern_object[5]
        self.props = pattern_object[6]

    def convert(self, content, props, *args, **kwargs) -> dict:
        """ """
        block = {
            "type": self.blocktype,
            "props": process_props(props),
            "data": content
        }
        
        ## findall
        if self.process == "findall":
            m = self.pattern.findall(content)
            if m:
                if self.blocktype == "blockquote":
                    m = [_.lstrip(" ") for _ in m]
                    block["data"] = "".join(m)
                else:
                    block["data"] = m
        ## headerbody
        elif self.process == "headerbody":
            m = self.pattern.match(content)
            if m:
                if self.blocktype == "dlist":
                    block["data"] = m.groupdict()
                    definition = m.group("definition").split("\n")
                    definition = [_.lstrip(": ") for _ in definition]
                    block["data"]["definition"] = definition
                elif self.blocktype == "footnote" or self.blocktype == "admonition":
                    data = m.group("data").split("\n")
                    data = [_.lstrip(" ") for _ in data]
                    block["data"] = "\n".join(data)
                    
                    for p in self.props:
                        if p == "data":
                            continue
                        block["props"].update({p: m.group(p)})
                        
                elif self.blocktype == "table":
                    block["data"] = {}
                    for p in self.props:
                        if p == "data":
                            continue
                        block["data"].update({p: m.group(p)})
                else:
                    block["data"] = m.groupdict()
        ## oneshots
        elif self.process == "oneshot":
            m = self.pattern.match(content)
            if m:
                if "data" in self.props:
                    block["data"] = m.group("data")
                else:
                    block["data"] = m.groupdict()
                for p in self.props:
                    if p == "data":
                        continue
                    block["props"].update({p: m.group(p)})
        ## captureprocess
        elif self.process == "captureprocess":
            m = self.pattern.match(content)
            if m:
                block["data"] = m.group("data")
                for p in self.props:
                    if p == "data":
                        continue
                    block["props"].update({p: m.group(p)})
            
        return block


"""
(?:^\[\^(?P<index>.+?)\]:\n)

when we grab a paragraph, make sure to merge the lines so that there are non newline characters 
inside of a pblock
"""
PROC_PATTERNS = [
    ["meta", r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)', re.MULTILINE | re.DOTALL, "captureprocess", False, False, ["data"]],
    ["code", r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))', re.MULTILINE | re.DOTALL, "captureprocess", False, False, ["language", "data"]],
    
    ["dlist", r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", False, True, ["definition", "term"]], # 
    ["footnote", r'^\[\^(?P<index>.+?)\]:\s*\n(?P<data>(?: {4,}.*(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", True, True, ["index", "data"]], # capture, header, dedent
    ["admonition", r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<data>(?:^ {4,}.*?(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", True, True, ["type", "title", "data"]], # capture, header, dedent
    ["table", r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})', re.MULTILINE | re.DOTALL, "headerbody", False, True, ["header", "body"]],
    
    ["hr", r'^(?P<data>[\*\-]{3,})\s*(?:\n|$)', re.MULTILINE | re.DOTALL, "oneshot", False, False, ["data"]],
    ["heading", r'^(?P<level>\#{1,})\s+(?P<data>.*?)(?:$|\n)', re.MULTILINE | re.DOTALL, "oneshot", False, True, ["level", "data"]],
    ["image", r'^\!\[(?P<alt>.*?)?\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)', re.MULTILINE | re.DOTALL, "oneshot", False, False, ["alt", "data", "title"]],
    ["svg", r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>', re.MULTILINE | re.DOTALL, "oneshot", False, False, ["attrs", "data"]],
    
    ["paragraph", r'(?P<data>.*?)(?:\n|\n\n|$)', re.MULTILINE | re.DOTALL, "oneshot", False, True, ["data"]],
    
    ["ulist", r'(?<=^- ).*?(?:\n|$)(?: {2}.*(?:\n|$))*', re.MULTILINE, "findall", True, True, []],
    ["olist", r'(?:(?<=^\d\. )|(?<=^\d\d\. )).*?(?:\n|$)(?: {2}.*(?:\n|$))*', re.MULTILINE, "findall", True, True, []],
    ["blockquote", r'(?<=^>).*(?:\n|$)', re.MULTILINE, "findall", True, True, []],
]


def BuildPatternDict(patterns:list=[])-> dict:
    pattern_list = [(p[0], Patties(p)) for p in patterns]
    return dict(pattern_list)


PATTERN_DICT = BuildPatternDict(PROC_PATTERNS)