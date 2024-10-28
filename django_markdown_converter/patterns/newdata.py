import re
from textwrap import dedent
from django_markdown_converter.patterns.inlines.parser import convert_inline


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

## lambdas
LAMBDA_REMOVE_PREFIX = lambda x, amount: "\n".join([_[amount:] for _ in x.split("\n")])
LAMBDA_REMOVE_PREFIX_2 = lambda x: LAMBDA_REMOVE_PREFIX(x, 2)

def process_meta_values(content:str="")-> dict:
    PATTERN_RAW = r'^(?P<key>.*?)(?:\:\s*)(?P<value>.*?)(?:\n|$)'
    PATTERN = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)
    kvps = PATTERN.findall(content)
    if kvps:
        return dict(kvps)
    return {}

def between_quotes(content:str="")-> dict:
    PATTERN_RAW = r'(?:\")(.*?)(?:\")'
    PATTERN = re.compile(PATTERN_RAW)
    kvps = PATTERN.search(content)
    if kvps:
        return dict(kvps)
    return {}


"""
- data is between the open and close
- data is key value pairs that need to be processed
"""
META_PATTERN = {
    "name": "meta",
    "pattern": [
        r"^---*?\n",
        ("content", r".*?"),
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
    "data": ["content"],
    "processing": {
        "content": process_meta_values,
    },
}


"""
- data is between the open and close
- data is code that needs to converted using Pygments
- we can post process our code blocks the same as our images
"""
CODE_PATTERN = {
    "name": "code",
    "pattern": [
        r"^```",
        ("language", r"\S+"),
        r"?\n",
        ("content", r"(?:^.*?\n)+?"),
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
    "data": ["content"],
    "processing": {
        "content": lambda x: x,
    },
}

"""
- data has a specific structure
- has a prefix that needs to be removed
"""
DLIST_PATTERN = {
    "name": "dlist",
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
    "data": ["term", "definition"],
    "processing": {
        "term": lambda x: x.strip(),
        "definition": LAMBDA_REMOVE_PREFIX_2,
    },
}

"""
- data has a specific structure
- has a prefix that needs to be removed
"""
FOOTNOTE_PATTERN = {
    "name": "footnote",
    "pattern": [
        r"^\[\^",
        ("index", r".+?"),
        r"\]:\n",
        ("content", r"(?:^ {1,}.*?\n)+"),
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
    "data": ["content"],
    "processing": {
        "index": lambda x: int(x),
        "content": dedent,
    },
}

"""
- data has a specific structure
- has a prefix that needs to be removed
"""
ADMONITION_PATTERN = {
    "name": "admonition",
    "pattern": [
        r"^!!!",
        ("type", r" \S+"),
        r"?(?: \"",
        ("title", r".+?"),
        r"\")?\n",
        ("content", r"(?:^ {1,}.*?\n)+"),
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
    "data": ["content"],
    "processing": {
        "type": dedent,
        "title": lambda x: x,
        "content": dedent,
    },
}

def get_row(line:str="") -> list:
    """strip leading and trailing pipes,"""
    line = line.strip("|\n ")
    #return [convert_inline(_.strip()) for _ in line.split("|")]
    return [_.strip() for _ in line.split("|")]
    
def get_rows(chunk:str="")-> list:
    lines = chunk.split("\n")
    return [get_row(line) for line in lines if len(line)]

TABLE_PATTERN = {
    "name": "table",
    "pattern": [
        ("header", r"^\|.*?\|\n"),
        ("break", r"^\|.*?\|\n"),
        ("content", r"(?:^\|.*?\|\n)+"),
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
    "data": ["header", "content"],
    "processing": {
        "header": get_row,
        "break": get_row,
        "content": get_rows,
    },
}

HR_PATTERN = {
    "name": "hr",
    "pattern": [
        ("content", r"^[\*\-]{3,}\n"),
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
    "data": ["content"],
    "processing": {
        "content": lambda x: ""
    },
}

HEADING_PATTERN = {
    "name": "heading",
    "pattern": [
        ("level", r"^\#{1,}"),
        ("content", r".*?"),
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
    "props": ["level", "content"],
    "data": ["content"],
    "processing": {
        "level": lambda x: len(x),
        "content": lambda x: x.strip(),
    },
}

IMAGE_PATTERN = {
    "name": "image",
    "pattern": [
        r"^\!\[",
        ("alt", r".*?"),
        r"?\]\(",
        ("src", r"\S*"),
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
    "data": ["src"],
    "processing": {
        "alt": lambda x: x,
        "title": lambda x: x,
        "src": lambda x: x,
    },
}

SVG_PATTERN = {
    "name": "svg",
    "pattern": [
        r"^<svg",
        ("attrs", r"[^>]*"),
        r">",
        ("content", r".*?"),
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
    "processing": {
        "attrs": lambda x: x,
        "content": lambda x: x,
    },
}

HTML_PATTERN = {
    "name": "svg",
    "pattern": [
        r"^<(?P<htmltag>\S+)",
        ("attrs", r"[^>]*"),
        r">",
        ("content", r".*?"),
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
    "data": ["content"],
    "processing": {
        "attrs": lambda x: x,
        "content": lambda x: x,
    },
}

def process_list(content):
    padding_multiline = " "*3
    padding_indented = " "*4
    pattern = re.compile(r"(?:^(?:(?:\d{1,}\. )|(?:- ))+)(?P<item>.*\n(?:^ .*?\n)*)", re.MULTILINE)
    items = pattern.findall(content)
    newitems = []
    
    for item in items:
        lines = []
        for line in item.splitlines():
            if line.startswith(padding_indented):
                line = line.removeprefix(padding_indented)
            else:
                line = line.removeprefix(padding_multiline)
            lines.append(line)
        lines = "\n".join(lines)
        newitems.append({"name": "item", "data": lines})
    return newitems

ULIST_PATTERN = {
    "name": "ulist",
    "pattern": [
        ("items", r"(?:^- .*\n(?:^ .*?\n)*)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": True,
        "hasInlineMarkup": False,
    },
    "props": ["items", "level", "marker", "content"],
    "data": [],
    "processing": {
        "items": process_list,
    },
}


OLIST_PATTERN = {
    "name": "olist",
    "pattern": [
        ("items", r"(?:^\d+\. .*\n(?:^ .*?\n)*)+"),
    ],
    "flags": {
        "MULTILINE": True,
        "DOTALL": False,
    },
    "attributes": {
        "hasNested": False,
        "hasInlineMarkup": False,
    },
    "props": ["items", "level", "marker", "content"],
    "data": [],
    "processing": {
        "items": process_list,
    },
}

BLOCKQUOTE_PATTERN = {
    "name": "blockquote",
    "pattern": [
        ("content", r"(?:^>.*?\n)+"),
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
    "data": ["content"],
    "processing": {
        "content": LAMBDA_REMOVE_PREFIX_2,
    },
}

PARAGRAPH_PATTERN = {
    "name": "paragraph",
    "pattern": [
        ("content", r"^.+?\n"),
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
    "data": ["content"],
    "processing": {
        "content": lambda x: x,
    },
}

EMPTYLINE_PATTERN = {
    "name": "emptyline",
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
    "processing": {},
}

NEWLINE_PATTERN = {
    "name": "newline",
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
    "processing": {},
}

NONE_PATTERN = {
    "name": "none",
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
    "processing": {},
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