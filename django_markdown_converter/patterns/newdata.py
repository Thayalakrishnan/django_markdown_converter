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
        r"^---*?\n",
        ("data", r".*?"),
        r"^---*?\n^",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": ["data"],
}

CODE_PATTERN = {
    "type": "code",
    "pattern": [
        r"^```",
        ("language", r"\S+"),
        r"?\n",
        ("data", r"(?:^.*?\n)+?"),
        r"^```\n",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["language"],
    "data": ["data"],
}

DLIST_PATTERN = {
    "type": "dlist",
    # prefix:  ": "
    "pattern": [
        ("term", r"^.*?\n"),
        ("definition", r"(?:^\: .*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": True,
    },
    "props": [],
    "data": ["definition", "term"],
}

FOOTNOTE_PATTERN = {
    "type": "footnote",
    "pattern": [
        r"^\[\^",
        ("index", r".+?"),
        r"\]:\n",
        ("data", r"(?:^ {1,}.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": True,
        "hasInlineMarkup": False,
    },
    "props": ["index"],
    "data": ["data"],
}

ADMONITION_PATTERN = {
    "type": "admonition",
    "pattern": [
        r"^!!!",
        ("type", r" \S+"),
        r"?",
        ("title", r" \".+?\""),
        r"?\n",
        ("data", r"(?:^ {1,}.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": True,
        "hasInlineMarkup": False,
    },
    "props": ["type", "title"],
    "data": ["data"],
}

TABLE_PATTERN = {
    "type": "table",
    "pattern": [
        ("header", r"^\|.*?\|\n"),
        ("break", r"^\|.*?\|\n"),
        ("body", r"(?:^\|.*?\|\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": True,
    },
    "props": [],
    "data": ["header", "body"],
}

HR_PATTERN = {
    "type": "hr",
    "pattern": [
        ("data", r"^[\*\-]{3,}\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": ["data"],
}

HEADING_PATTERN = {
    "type": "heading",
    "pattern": [
        ("level", r"^\#{1,}"),
        ("data", r".*?"),
        r"\n",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": True,
    },
    "props": ["level", "data"],
    "data": ["data"],
}

IMAGE_PATTERN = {
    "type": "image",
    "pattern": [
        r"^\!\[",
        ("alt", r".*?"),
        r"?\]\(",
        ("data", r"\S*"),
        r"(?: *?\"",
        ("title", r".*?"),
        r"\")?\)\n",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["alt", "title"],
    "data": ["data"],
}

SVG_PATTERN = {
    "type": "svg",
    "pattern": [
        r"^<svg",
        ("attrs", r"[^>]*"),
        r">",
        ("data", r".*?"),
        r"</svg>\n",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["attrs"],
    "data": ["data"],
}

HTML_PATTERN = {
    "type": "svg",
    "pattern": [
        r"^<(?P<htmltag>\S+)",
        ("attrs", r"[^>]*"),
        r">",
        ("data", r".*?"),
        r"</(?P=htmltag)>\n",
        r"(?=^\n)",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": True,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["attrs"],
    "data": ["data"],
}

ULIST_PATTERN = {
    "type": "ulist",
    "check": r'(?:^ *- +.*$)+',
    "pattern": [
        ("item", r"^- .*\n(?:^ .*?\n)*"),
        r"+",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": True,
        "hasInlineMarkup": False,
    },
    "props": ["level", "marker", "content"],
    "data": [],
}

OLIST_PATTERN = {
    "type": "olist",
    "check": r'(?:^ *\d+\. +.*$)+',
    "pattern": [
        ("item", r"^\d+\. .*\n(?:^ .*?\n)*"),
        r"+",
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["level", "marker", "content"],
    "data": [],
}

BLOCKQUOTE_PATTERN = {
    "type": "blockquote",
    "pattern": [
        ("data", r"(?:^>.*?\n)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": True,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": ["data"],
}

PARAGRAPH_PATTERN = {
    "type": "paragraph",
    "pattern": [
        ("data", r"^.+?\n"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": True,
    },
    "props": [],
    "data": ["data"],
}

EMPTYLINE_PATTERN = {
    "type": "emptyline",
    "pattern": [
        r"^\n",
    ],
    "flags": {
        "MULTILINE": False,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": [],
}

NEWLINE_PATTERN = {
    "type": "newline",
    "pattern": [
        r"\n",
    ],
    "flags": {
        "MULTILINE": False,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": [],
}

NONE_PATTERN = {
    "type": "none",
    "pattern": [
        r".",
    ],
    "flags": {
        "MULTILINE": False,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": [],
    "data": [],
}

PATTERNS = [
    CODE_PATTERN,
    META_PATTERN,
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
    EMPTYLINE_PATTERN,
    NEWLINE_PATTERN,
    PARAGRAPH_PATTERN,
    NONE_PATTERN,
]