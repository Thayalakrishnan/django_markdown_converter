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

    def convert(self, content, props, *args, **kwargs) -> dict:
        """ """
        block = {
            "type": self.blocktype,
            "props": process_props(props),
            "data": content
        }
        
        if self.process == "findall":
            m = self.pattern.findall(content)
            if m:
                if self.blocktype == "blockquote":
                    m = [_.lstrip(" ") for _ in m]
                    block["data"] = "".join(m)
                else:
                    block["data"] = m
        elif self.process == "headerbody":
            m = self.pattern.match(content)
            if m:
                if self.blocktype == "dlist":
                    block["data"] = m.groupdict()
                    definition_data = m.group("definition").split("\n")
                    definition_data = [_.lstrip(": ") for _ in definition_data]
                    block["data"]["definition"] = definition_data
                elif self.blocktype == "footnote" or self.blocktype == "admonition":
                    block["data"] = m.groupdict()
                    content_data = m.group("content").split("\n")
                    content_data = [_.lstrip(" ") for _ in content_data]
                    block["data"]["content"] = "\n".join(content_data)
                #elif self.blocktype == "admonition":
                #    block["data"] = m.groupdict()
                elif self.blocktype == "table":
                    block["data"] = m.groupdict()
                else:
                    block["data"] = m.groupdict()
        elif self.process == "oneshot":
            m = self.pattern.match(content)
            if m:
                block["data"] = m.groupdict()
        elif self.process == "captureprocess":
            m = self.pattern.match(content)
            if m:
                block["data"] = m.groupdict()
            
        return block


"""
(?:^\[\^(?P<index>.+?)\]:\n)

when we grab a paragraph, make sure to merge the lines so that there are non newline characters 
inside of a pblock
"""
PROC_PATTERNS = [
    ["meta", r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)', re.MULTILINE | re.DOTALL, "captureprocess", False, False],
    ["code", r'(?:^```(?P<language>\S+)?\s*\n)(?P<content>(?:^.*?\n)+)(?:^```.*?(\n|$))', re.MULTILINE | re.DOTALL, "captureprocess", False, False],
    
    ["dlist", r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", False, True],
    ["footnote", r'^\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", True, True], # capture, header, dedent
    ["admonition", r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<content>(?:^ {4,}.*?(?:\n|$))+)', re.MULTILINE | re.DOTALL, "headerbody", True, True], # capture, header, dedent
    ["table", r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})', re.MULTILINE | re.DOTALL, "headerbody", False, True],
    
    ["hr", r'^(?P<content>[\*\-]{3,})\s*(?:\n|$)', re.MULTILINE | re.DOTALL, "oneshot", False, False],
    ["heading", r'^(?P<level>\#{1,})\s+(?P<content>.*?)(?:$|\n)', re.MULTILINE | re.DOTALL, "oneshot", False, True],
    ["image", r'^\!\[(?P<alt>.*?)\]\((?P<src>\S*?)\s(?P<title>.*?)?\)', re.MULTILINE | re.DOTALL, "oneshot", False, False],
    ["svg", r'^<svg\s(?P<attrs>[^>]*)>(?P<content>.*?)</svg>', re.MULTILINE | re.DOTALL, "oneshot", False, False],
    ["paragraph", r'(?P<content>.*?)(?:\n|\n\n|$)', re.MULTILINE | re.DOTALL, "oneshot", False, True],
    
    ["ulist", r'(?<=^- ).*?(?:\n|$)(?: {2}.*(?:\n|$))*', re.MULTILINE, "findall", True, True],
    ["blockquote", r'(?<=^>).*(?:\n|$)', re.MULTILINE, "findall", True, True],
    ["olist", r'(?:(?<=^\d\. )|(?<=^\d\d\. )).*?(?:\n|$)(?: {2}.*(?:\n|$))*', re.MULTILINE, "findall", True, True],
]


def BuildPatternDict(patterns:list=[])-> dict:
    pattern_list = [(p[0], Patties(p)) for p in patterns]
    return dict(pattern_list)


PATTERN_DICT = BuildPatternDict(PROC_PATTERNS)