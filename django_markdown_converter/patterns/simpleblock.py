import re

"""
"""


META_PATTERN = (r'^---.*?^---.*?(?=^\n)', re.MULTILINE | re.DOTALL)


CODE_PATTERN = (r'(?:^```.*?$\n)(?:.*?$\n)+?(?:^```)', re.MULTILINE)
TABLE_PATTERN = (r'(?:^\|.*?\| *?$\n)+(?:\{.*?\})?', re.MULTILINE)
BLOCKQUOTE_PATTERN = (r'(?:^> *?.*?$\n)+(?:\{.*?\})?', re.MULTILINE)
HR_PATTERN = (r'^(?:[\*\-]{3,} *(?:\s?\{.*?\})?$)', re.MULTILINE)
HEADING_PATTERN = (r'^\#+\s+.*?$\n', re.MULTILINE)
IMAGE_PATTERN = (r'^!\[.*?\]\(.*?\)', re.MULTILINE | re.DOTALL)
SVG_PATTERN = (r'^<svg\s[^>]*>(?:.*?)</svg>', re.MULTILINE | re.DOTALL)
ORDERED_LIST_PATTERN = (r'(?:^ *\d+\. +.*?\n)+(?=^\n)?', re.MULTILINE | re.DOTALL)
PARAGRAPH_PATTERN = (r'(?:.*?)(?:\n|\n\n|$)', re.MULTILINE | re.DOTALL)

UNORDERED_LIST_PATTERN = (r'(?:^ *- +.*?\n)+(?=^\n)?', re.MULTILINE | re.DOTALL)
ADMONITION_PATTERN = (r'(?:^!!!.*?\n$)', re.MULTILINE | re.DOTALL)


DEFINITIONLIST_PATTERN = (r'(?:^.+?$\n)(?:\: .*?$\n)+?(?:\{.*?\})?', re.MULTILINE)
DEFINITIONLIST_PATTERN = (r'^.+?$(?:\n\: .*?$)+(?:\n\{.*?\})?', re.MULTILINE)
DEFINITIONLIST_PATTERN = (r'^.+?$\n(?:\: .*?$\n)+(?:\{.*?\})?', re.MULTILINE)


FOOTNOTE_PATTERN = (r'(?:^\[\^.*?$\n)(?:.*?)(?=^\n)', re.MULTILINE | re.DOTALL)

"""
"""
BLOCK_PATTERNS = [
    ["meta", META_PATTERN, ["content"], False],
    ["definition list", DEFINITIONLIST_PATTERN, ["term", "definition", "attrs"], True],
    ["footnote", FOOTNOTE_PATTERN, ["index", "content", "attrs"], True],
    ["admonition", ADMONITION_PATTERN, ["attrs"], True],
    ["code", CODE_PATTERN, ["attrs"], True],
    ["table", TABLE_PATTERN, ["header", "body", "break", "attrs"], True],
    ["blockquote", BLOCKQUOTE_PATTERN, ["attrs"], True],
    ["hr", HR_PATTERN, ["attrs"], True],
    ["heading", HEADING_PATTERN, ["attrs"], True],
    ["image", IMAGE_PATTERN, ["attrs"], True],
    ["svg", SVG_PATTERN, ["attrs"], True],
    ["unordered list", UNORDERED_LIST_PATTERN, ["attrs"], True],
    ["ordered list", ORDERED_LIST_PATTERN, ["attrs"], True],
    ["paragraph", PARAGRAPH_PATTERN, ["attrs", "content"], True],
]

# compile PATTERNS
for p in BLOCK_PATTERNS:
    pattern = p[1][0]
    flags = p[1][1]
    p[1] = re.compile(pattern, flags)
