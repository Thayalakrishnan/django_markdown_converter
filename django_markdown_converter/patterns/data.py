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
    "check": r'^---.*?^---$',
    "pattern": r'^(?:---\s*)(?:\n)(?P<data>.*?)(?:---\s*)(?:\n|$)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

CODE_PATTERN = {
    "type": "code",
    "check": r'^```.*?^```$',
    "pattern": r'(?:^```(?P<language>\S+)?\s*\n)(?P<data>(?:^.*?\n)+)(?:^```.*?(\n|$))',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["language"],
    "data": ["data"],
}

DLIST_PATTERN = {
    "type": "dlist",
    "check": r'^.+?$\n(?:\: .*$)',
    "pattern": r'(?P<term>^.*?\n)(?P<definition>(?:(?=^\: ).*?(?:\n|$))+)',
    "flags": re.MULTILINE,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["definition", "term"],
}

FOOTNOTE_PATTERN = {
    "type": "footnote",
    "check": r'^\[\^\d+\]\:\n.*$',
    "pattern": r'^\[\^(?P<index>.+?)\]:\s*\n(?P<data>(?: {4}.*(?:\n|$))+)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["index"],
    "data": ["data"],
}

ADMONITION_PATTERN = {
    "type": "admonition",
    "check": r'(?:^!!!.*$)',
    "pattern": r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<data>(?:^ {4}.*?(?:\n|$))+)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["type", "title"],
    "data": ["data"],
}

TABLE_PATTERN = {
    "type": "table",
    "check": r'(?:^\|.*?\|\s*?$\n?)+',
    "pattern": r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["header", "body"],
}

HR_PATTERN = {
    "type": "hr",
    "check": r'^(?:[\*\-]{3,}$)',
    "pattern": r'^(?P<data>[\*\-]{3,})\s*(?:\n|$)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

HEADING_PATTERN = {
    "type": "heading",
    "check": r'^\#+\s+.*?$',
    "pattern": r'^(?P<level>\#{1,})\s+(?P<data>.*?)(?:$|\n)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": ["level", "data"],
    "data": ["data"],
}

IMAGE_PATTERN = {
    "type": "image",
    "check": r'^!\[.*?\]\(.*?\)',
    "pattern": r'^\!\[\s*(?P<alt>.*?)?\s*\]\((?P<data>\S*)\s*(?:\"(?P<title>.*?)\")?\)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["alt", "title"],
    "data": ["data"],
}

SVG_PATTERN = {
    "type": "svg",
    "check": r'^<svg\s[^>]*>(?:.*?)</svg>',
    "pattern": r'^<svg\s(?P<attrs>[^>]*)>(?P<data>.*?)</svg>',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": ["attrs"],
    "data": ["data"],
}

ULIST_PATTERN = {
    "type": "ulist",
    "check": r'(?:^ *- +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": re.MULTILINE,
    "addToLookup": True,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

OLIST_PATTERN = {
    "type": "olist",
    "check": r'(?:^ *\d+\. +.*$)+',
    "pattern": r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))',
    "flags": re.MULTILINE,
    "addToLookup": True,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": ["level", "marker", "content"],
    "data": [],
}

BLOCKQUOTE_PATTERN = {
    "type": "blockquote",
    "check": r'(?:^>.*$)+',
    "pattern": r'(?<=^>).*(?:\n|$)',
    "flags": re.MULTILINE,
    "addToLookup": True,
    "hasNested": True,
    "hasInlineMarkup": False,
    "props": [],
    "data": [],
}

PARAGRAPH_PATTERN = {
    "type": "paragraph",
    "check": r'.*',
    #"pattern": r'(?P<data>.*?)(?:\n|\n\n|$)',
    "pattern": r'(?P<data>.*)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": True,
    "hasNested": False,
    "hasInlineMarkup": True,
    "props": [],
    "data": ["data"],
}
