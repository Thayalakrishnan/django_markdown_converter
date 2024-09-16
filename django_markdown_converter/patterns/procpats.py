import re

from django_markdown_converter.patterns.blocks.table import TablePattern
from django_markdown_converter.patterns.blocks.admonition import AdmonitionPattern
from django_markdown_converter.patterns.blocks.footnote import FootnotePattern
from django_markdown_converter.patterns.blocks.dlist import DListPattern
from django_markdown_converter.patterns.blocks.code import CodePattern
from django_markdown_converter.patterns.blocks.meta import MetaPattern
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern
from django_markdown_converter.patterns.blocks.list import ListPattern
from django_markdown_converter.patterns.blocks.heading import HeadingPattern
from django_markdown_converter.patterns.blocks.image import ImagePattern
from django_markdown_converter.patterns.blocks.svg import SVGPattern
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern
from django_markdown_converter.patterns.blocks.hr import HRPattern




"""
fenced: 
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
6 | props: values extracted from the pattern that are merged with the other props

fenced
headerbody
oneshot
findall


^([^\n:]+?)(?:\n: (.*?))(?:\n: (.*?))*     # Capture subsequent lines that start with ': ' (if any)
"""

PROC_PATTERNS = [
    {
        "type": "meta",
        "class": MetaPattern,
        "check": r'^---.*?^---$',
        "pattern": r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "fenced",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["data"],
    },
    {
        "type": "code",
        "class": CodePattern,
        "check": r'^```.*?^```$',
        "pattern": r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "fenced",
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["language", "data"],
    },
    {
        "type": "dlist",
        "class": DListPattern,
        "check": r'^.+?$\n(?:\: .*$)',
        #"pattern": r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?(?:\n|$))+)',
        "pattern": r'(?P<term>^.*?\n)(?P<definition>(?:(?=^\: ).*?(?:\n|$))+)',
        "flags": re.MULTILINE, # might need to add dotall back
        "process": "headerbody",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["definition", "term"],
    },
    {
        "type": "footnote",
        "class": FootnotePattern,
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
        "class": AdmonitionPattern,
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
        "class": TablePattern,
        "check": r'(?:^\|.*?\|\s*?$\n?)+',
        "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})',
        "flags": re.MULTILINE | re.DOTALL,
        "process": "table",
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["header", "body"],
    },
    {
        "type": "hr",
        "class": HRPattern,
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
        "class": HeadingPattern,
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
        "class": ImagePattern,
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
        "class": SVGPattern,
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
        "class": ListPattern,
        "check": r'(?:^ *- +.*$)+',
        "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
        "flags": re.MULTILINE,
        "process": "findall",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": ["level", "marker", "content"],
    },
    {
        "type": "olist",
        "class": ListPattern,
        "check": r'(?:^ *\d+\. +.*$)+',
        "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
        "flags": re.MULTILINE,
        "process": "findall",
        "hasNested": True,
        "hasInlineMarkup": True,
        "props": ["level", "marker", "content"],
    },
    {
        "type": "blockquote",
        "class": BlockquotePattern,
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
        "class": ParagraphPattern,
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
        inst = p["class"](p)
        if inst:
            pattern_list.append(inst)
    return pattern_list

PATTERN_LIST = BuildPatternList(PROC_PATTERNS)