import re

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
    "pattern": [
        ("", r"^---*?\n"),
        ("data", r".*?"),
        ("", r"^---*?\n^"),
        ("", r"\n|$"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

CODE_PATTERN = {
    "type": "code",
    "check": r'^```.*?^```$',
    #"pattern": r'(?:^```)(?P<language>\S+)?\n(?P<data>(?:^.*?\n)+?)(?:^```\n)',
    "pattern": [
        ("", r"^```"),
        ("language", r"\S+"),
        ("", r"?\n"),
        ("data", r"(?:^.*?\n)+?"),
        ("", r"^```\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["language"],
    "data": ["data"],
}

DLIST_PATTERN = {
    "type": "dlist",
    "check": r'^.+?$\n(?:\: .*$)',
    #"pattern": r'(?P<term>^.*?\n)(?P<definition>(?:^\: .*?\n)+)',
    # prefix:  ": "
    "pattern": [
        ("term", r"^.*?\n"),
        ("definition", r"(?:^\: .*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["definition", "term"],
}

FOOTNOTE_PATTERN = {
    "type": "footnote",
    #"pattern": r'^\[\^(?P<index>.+?)\]:\n(?P<data>(?: {1,}.*?\n)+)',
    "pattern": [
        ("", r"^\[\^"),
        ("index", r".+?"),
        ("", r"\]:\n"),
        ("data", r"(?:^ {1,}.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["index"],
    "data": ["data"],
}

ADMONITION_PATTERN = {
    "type": "admonition",
    #"pattern": r'(?:^!!!)(?P<type> \S+)?(?: \"(?P<title>.+?)\")?\n(?P<data>(?:^ {1,}.*?\n)+)',
    "pattern": [
        ("", r"^!!!"),
        ("type", r" \S+"),
        ("", r"?"),
        ("title", r" \".+?\""),
        ("", r"?\n"),
        ("data", r"(?:^ {1,}.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["type", "title"],
    "data": ["data"],
}

TABLE_PATTERN = {
    "type": "table",
    "check": r'(?:^\|.*?\|\s*?$\n?)+',
    "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n)+)',
    "pattern": [
        ("header", r"^\|.*?\|\n"),
        ("break", r"^\|.*?\|\n"),
        ("body", r"(?:^\|.*?\|\n)+"),
        ("", r"?"),
        ("title", r" \".+?\""),
        ("", r"?\n"),
        ("data", r"(?:^ {1,}.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["header", "body"],
}

HR_PATTERN = {
    "type": "hr",
    #"pattern": r'(?P<data>^[\*\-]{3,})\n',
    "pattern": [
        ("data", r"^[\*\-]{3,}"),
        ("", r"\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

HEADING_PATTERN = {
    "type": "heading",
    #"pattern": r'(?P<level>^\#{1,})(?P<data>.*?)\n',
    "pattern": [
        ("level", r"^\#{1,}"),
        ("data", r".*?"),
        ("", r"\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": ["level", "data"],
    "data": ["data"],
}

IMAGE_PATTERN = {
    "type": "image",
    "check": r'^\!\[.*?\]\(.*?\)',
    #"pattern": r'^\!\[\s*(?P<alt>.*?)?\s*\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)',
    "pattern": r'^\!\[(?P<alt>.*?)?\]\((?P<data>\S*)(?: *?\"(?P<title>.*?)\")?\)',
    "pattern": [
        ("", r"^\!\["),
        ("alt", r".*?"),
        ("", r"?\]\("),
        ("data", r"\S*"),
        ("", r"(?: *?\""),
        ("title", r".*?"),
        ("", r"\")?\)\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["alt", "title"],
    "data": ["data"],
}

SVG_PATTERN = {
    "type": "svg",
    "check": r'^<svg\s[^>]*>(?:.*?)</svg>',
    "pattern": r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>',
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["attrs"],
    "data": ["data"],
}

ULIST_PATTERN = {
    "type": "ulist",
    "check": r'(?:^ *- +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    #"hasNested": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

OLIST_PATTERN = {
    "type": "olist",
    "check": r'(?:^ *\d+\. +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    #"hasNested": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

BLOCKQUOTE_PATTERN = {
    "type": "blockquote",
    "check": r'(?:^>.*$)+',
    #"pattern": r'(?<=^>).*(?:\n|$)',
    "pattern": r'(?P<data>(?:^>.*?\n)+)',
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

PARAGRAPH_PATTERN = {
    "type": "paragraph",
    "check": r'.*',
    "pattern": r'(?P<data>.*)',
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["data"],
}
