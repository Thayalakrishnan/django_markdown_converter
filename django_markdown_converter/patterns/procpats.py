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
when we grab a paragraph, make sure to merge the lines so that there are non newline characters 
inside of a pblock

0 | type
1 | class
2 | check
3 | pattern
4 | flags
5 | has Nested
6 | has Inline Markup
7 | props: values extracted from the pattern that are merged with the other props
8 | data: 
"""

PROC_PATTERNS = [
    {
        "type": "meta",
        "class": MetaPattern,
        "check": r'^---.*?^---$',
        "pattern": r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": [],
        "data": ["data"],
    },
    {
        "type": "code",
        "class": CodePattern,
        "check": r'^```.*?^```$',
        "pattern": r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["language"],
        "data": ["data"],
    },
    {
        "type": "dlist",
        "class": DListPattern,
        "check": r'^.+?$\n(?:\: .*$)',
        #"pattern": r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?(?:\n|$))+)',
        "pattern": r'(?P<term>^.*?\n)(?P<definition>(?:(?=^\: ).*?(?:\n|$))+)',
        "flags": re.MULTILINE, # might need to add dotall back
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": [],
        "data": ["definition", "term"],
    },
    {
        "type": "footnote",
        "class": FootnotePattern,
        "check": r'^\[\^\d+\]\:\n.*$',
        "pattern": r'^\[\^(?P<index>.+?)\]:\s*\n(?P<data>(?: {4,}.*(?:\n|$))+)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": True,
        "hasInlineMarkup": False,
        "props": ["index"],
        "data": ["data"],
    },
    {
        "type": "admonition",
        "class": AdmonitionPattern,
        "check": r'(?:^!!!.*$)',
        "pattern": r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<data>(?:^ {4,}.*?(?:\n|$))+)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": True,
        "hasInlineMarkup": False,
        "props": ["type", "title"],
        "data": ["data"],
    },
    {
        "type": "table",
        "class": TablePattern,
        "check": r'(?:^\|.*?\|\s*?$\n?)+',
        "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": [],
        "data": ["header", "body"],
    },
    {
        "type": "hr",
        "class": HRPattern,
        "check": r'^(?:[\*\-]{3,}$)',
        "pattern": r'^(?P<data>[\*\-]{3,})\s*(?:\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": [],
        "data": ["data"],
    },
    {
        "type": "heading",
        "class": HeadingPattern,
        "check": r'^\#+\s+.*?$',
        "pattern": r'^(?P<level>\#{1,})\s+(?P<data>.*?)(?:$|\n)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": ["level", "data"],
        "data": ["data"],
    },
    {
        "type": "image",
        "class": ImagePattern,
        "check": r'^!\[.*?\]\(.*?\)',
        "pattern": r'^\!\[(?P<alt>.*?)?\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["alt", "title"],
        "data": ["data"],
    },
    {
        "type": "svg",
        "class": SVGPattern,
        "check": r'^<svg\s[^>]*>(?:.*?)</svg>',
        "pattern": r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": False,
        "props": ["attrs"],
        "data": ["data"],
    },
    {
        "type": "ulist",
        "class": ListPattern,
        "check": r'(?:^ *- +.*$)+',
        "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
        "flags": re.MULTILINE,
        "hasNested": True,
        "hasInlineMarkup": False,
        "props": ["level", "marker", "content"],
        "data": [],
    },
    {
        "type": "olist",
        "class": ListPattern,
        "check": r'(?:^ *\d+\. +.*$)+',
        "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
        "flags": re.MULTILINE,
        "hasNested": True,
        "hasInlineMarkup": False,
        "props": ["level", "marker", "content"],
        "data": [],
    },
    {
        "type": "blockquote",
        "class": BlockquotePattern,
        "check": r'(?:^>.*$)+',
        "pattern": r'(?<=^>).*(?:\n|$)',
        "flags": re.MULTILINE,
        "hasNested": True,
        "hasInlineMarkup": False,
        "props": [],
        "data": [],
    },
    {
        "type": "paragraph",
        "class": ParagraphPattern,
        "check": r'.*',
        "pattern": r'(?P<data>.*?)(?:\n|\n\n|$)',
        "flags": re.MULTILINE | re.DOTALL,
        "hasNested": False,
        "hasInlineMarkup": True,
        "props": [],
        "data": ["data"],
    },
]


def BuildPatternList(patterns:list=[])-> tuple:
    pattern_list = []
    pattern_dict = {}
    
    for p in patterns:
        inst = p["class"](p)
        if inst:
            pattern_list.append(inst)
            pattern_dict[p["type"]] = inst
    return pattern_list, pattern_dict

PATTERN_LIST, PATTERN_LOOKUP = BuildPatternList(PROC_PATTERNS)