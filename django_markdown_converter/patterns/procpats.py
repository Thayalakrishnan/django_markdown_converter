import re

from django_markdown_converter.patterns.classes.base import CaptureProcessPattern, FindAllPattern, OneShotPattern, HeaderBodyPattern

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

(?:^\[\^(?P<index>.+?)\]:\n)

when we grab a paragraph, make sure to merge the lines so that there are non newline characters 
inside of a pblock

[type, pattern, flags, process type, has Nested, has Inline Markup, props],

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

PROC_PATTERNS = [
    {
        "type": "meta",
        "check": r'^---.*?^---$',
        "pattern": r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "captureprocess",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["data"],
    },
    {
        "type": "code",
        "check": r'^```.*?^```$',
        "pattern": r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "captureprocess",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["language", "data"],
    },
    {
        "type": "dlist",
        "check": r'^.+?$\n(?:\: .*$)',
        "pattern": r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?(?:\n|$))+)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "headerbody",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["definition", "term"],
    },
    {
        "type": "footnote",
        "check": r'^\[\^\d+\]\:\n.*$',
        "pattern": r'^\[\^(?P<index>.+?)\]:\s*\n(?P<data>(?: {4,}.*(?:\n|$))+)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "headerbody",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": ["index", "data"],
    },
    {
        "type": "admonition",
        "check": r'(?:^!!!.*$)',
        "pattern": r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<data>(?:^ {4,}.*?(?:\n|$))+)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "headerbody",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": ["type", "title", "data"],
    },
    {
        "type": "table",
        "check": r'(?:^\|.*?\|\s*?$\n?)+',
        "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "headerbody",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["header", "body"],
    },
    {
        "type": "hr",
        "check": r'^(?:[\*\-]{3,}$)',
        "pattern": r'^(?P<data>[\*\-]{3,})\s*(?:\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "oneshot",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["data"],
    },
    {
        "type": "heading",
        "check": r'^\#+\s+.*?$',
        "pattern": r'^(?P<level>\#{1,})\s+(?P<data>.*?)(?:$|\n)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "oneshot",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["level", "data"],
    },
    {
        "type": "image",
        "check": r'^!\[.*?\]\(.*?\)',
        "pattern": r'^\!\[(?P<alt>.*?)?\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "oneshot",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["alt", "data", "title"],
    },
    {
        "type": "svg",
        "check": r'^<svg\s[^>]*>(?:.*?)</svg>',
        "pattern": r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "oneshot",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["attrs", "data"],
    },
    {
        "type": "ulist",
        "check": r'(?:^ *- +.*$)+',
        "pattern": r'(?<=^- ).*?(?:\n|$)(?: {2}.*(?:\n|$))*',
        "flags": re.MULTILINE,
        "process": "findall",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": [],
    },
    {
        "type": "olist",
        "check": r'(?:^ *\d+\. +.*$)+',
        "pattern": r'(?:(?<=^\d\. )|(?<=^\d\d\. )).*?(?:\n|$)(?: {2}.*(?:\n|$))*',
        "flags": re.MULTILINE,
        "process": "findall",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": [],
    },
    {
        "type": "blockquote",
        "check": r'(?:^>.*$)+',
        "pattern": r'(?<=^>).*(?:\n|$)',
        "flags": re.MULTILINE,
        "process": "findall",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": [],
    },
    {
        "type": "paragraph",
        "check": r'.*',
        "pattern": r'(?P<data>.*?)(?:\n|\n\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "oneshot",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["data"],
    },
]


def BuildPatternList(patterns:list=[])-> list:
    pattern_list = []
    
    for p in patterns:
        inst = None
        if p["process"] == "captureprocess":
            inst = CaptureProcessPattern(p)
        elif p["process"] == "headerbody":
            inst = HeaderBodyPattern(p)
        elif p["process"] == "oneshot":
            inst = OneShotPattern(p)
        elif p["process"] == "findall":
            inst = FindAllPattern(p)
        if inst:
            pattern_list.append(inst)
    return pattern_list

PATTERN_LIST = BuildPatternList(PROC_PATTERNS)