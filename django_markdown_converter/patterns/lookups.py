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

META_PATTERN = {
    "type": "meta",
    "class": MetaPattern,
    "check": r'^---.*?^---$',
    "pattern": r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

CODE_PATTERN = {
    "type": "code",
    "class": CodePattern,
    "check": r'^```.*?^```$',
    "pattern": r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["language"],
    "data": ["data"],
}

DLIST_PATTERN = {
    "type": "dlist",
    "class": DListPattern,
    "check": r'^.+?$\n(?:\: .*$)',
    "pattern": r'(?P<term>^.*?\n)(?P<definition>(?:(?=^\: ).*?(?:\n|$))+)',
    "flags": re.MULTILINE,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["definition", "term"],
}

FOOTNOTE_PATTERN = {
    "type": "footnote",
    "class": FootnotePattern,
    "check": r'^\[\^\d+\]\:\n.*$',
    "pattern": r'^\[\^(?P<index>.+?)\]:\s*\n(?P<data>(?: {4}.*(?:\n|$))+)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["index"],
    "data": ["data"],
}

ADMONITION_PATTERN = {
    "type": "admonition",
    "class": AdmonitionPattern,
    "check": r'(?:^!!!.*$)',
    "pattern": r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<data>(?:^ {4}.*?(?:\n|$))+)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["type", "title"],
    "data": ["data"],
}

TABLE_PATTERN = {
    "type": "table",
    "class": TablePattern,
    "check": r'(?:^\|.*?\|\s*?$\n?)+',
    "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["header", "body"],
}

HR_PATTERN = {
    "type": "hr",
    "class": HRPattern,
    "check": r'^(?:[\*\-]{3,}$)',
    "pattern": r'^(?P<data>[\*\-]{3,})\s*(?:\n|$)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

HEADING_PATTERN = {
    "type": "heading",
    "class": HeadingPattern,
    "check": r'^\#+\s+.*?$',
    "pattern": r'^(?P<level>\#{1,})\s+(?P<data>.*?)(?:$|\n)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": ["level", "data"],
    "data": ["data"],
}

IMAGE_PATTERN = {
    "type": "image",
    "class": ImagePattern,
    "check": r'^!\[.*?\]\(.*?\)',
    "pattern": r'^\!\[\s*(?P<alt>.*?)?\s*\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["alt", "title"],
    "data": ["data"],
}

SVG_PATTERN = {
    "type": "svg",
    "class": SVGPattern,
    "check": r'^<svg\s[^>]*>(?:.*?)</svg>',
    "pattern": r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["attrs"],
    "data": ["data"],
}

ULIST_PATTERN = {
    "type": "ulist",
    "class": ListPattern,
    "check": r'(?:^ *- +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": re.MULTILINE,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

OLIST_PATTERN = {
    "type": "olist",
    "class": ListPattern,
    "check": r'(?:^ *\d+\. +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": re.MULTILINE,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

BLOCKQUOTE_PATTERN = {
    "type": "blockquote",
    "class": BlockquotePattern,
    "check": r'(?:^>.*$)+',
    "pattern": r'(?<=^>).*(?:\n|$)',
    "flags": re.MULTILINE,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": [],
    "data": [],
}

PARAGRAPH_PATTERN = {
    "type": "paragraph",
    "class": ParagraphPattern,
    "check": r'.*',
    #"pattern": r'(?P<data>.*?)(?:\n|\n\n|$)',
    "pattern": r'(?P<data>.*)',
    "flags": re.MULTILINE | re.DOTALL,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["data"],
}


PROC_PATTERNS = [
    META_PATTERN,
    CODE_PATTERN,
    DLIST_PATTERN,
    FOOTNOTE_PATTERN,
    ADMONITION_PATTERN,
    TABLE_PATTERN,
    HR_PATTERN,
    HEADING_PATTERN,
    IMAGE_PATTERN,
    SVG_PATTERN,
    ULIST_PATTERN,
    OLIST_PATTERN,
    BLOCKQUOTE_PATTERN,
    PARAGRAPH_PATTERN,
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