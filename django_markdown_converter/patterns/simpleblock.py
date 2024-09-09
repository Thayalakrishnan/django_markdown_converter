import re

"""
"""

#META_PATTERN = (r'^---.*?^---$', re.MULTILINE | re.DOTALL)
#TABLE_PATTERN = (r'(?:^\|.*?\|$(?:\n|$))+(?:\{.*?\})?', re.MULTILINE)
#HR_PATTERN = (r'^(?:[\*\-]{3,}$)', re.MULTILINE)
#CODE_PATTERN = (r'(?:^```.*?$\n)(?:.*?$\n)+?(?:^```)', re.MULTILINE)


CODE_PATTERN = r'^```.*?^```$'
HEADING_PATTERN = r'^\#+\s+.*?$'
HR_PATTERN = r'^(?:[\*\-]{3,}$)'
TABLE_PATTERN = r'(?:^\|.*?\|\s*?$\n?)+'
ADMONITION_PATTERN = r'(?:^!!!.*$)'
BLOCKQUOTE_PATTERN = r'(?:^>.*$)+'
DEFINITIONLIST_PATTERN = r'^.+?$\n(?:\: .*$)'
FOOTNOTE_PATTERN = r'^\[\^\d+\]\:\n.*$'
IMAGE_PATTERN = r'^!\[.*?\]\(.*?\)'
ORDERED_LIST_PATTERN = r'(?:^ *\d+\. +.*$)+'
PARAGRAPH_PATTERN = r'.*'
SVG_PATTERN = r'^<svg\s[^>]*>(?:.*?)</svg>'
HTML_PATTERN = r'^<(?P<el>\S+)\s[^>]*>(?:.*?)</(?P=el)>' # to match generic HTML, ensure that it doesnt target codeblock html lol
UNORDERED_LIST_PATTERN = r'(?:^ *- +.*$)+'

"""
#["label", pattern, ["props"]],
"""
BLOCK_PATTERNS = [
    #["meta", META_PATTERN, ["content"]],
    ["definition list", DEFINITIONLIST_PATTERN, ["term", "definition", "props"]],
    ["footnote", FOOTNOTE_PATTERN, ["index", "content", "props"]],
    ["admonition", ADMONITION_PATTERN, ["props"]],
    ["code", CODE_PATTERN, ["props"]],
    ["table", TABLE_PATTERN, ["header", "body", "break", "props"]],
    ["blockquote", BLOCKQUOTE_PATTERN, ["props"]],
    ["hr", HR_PATTERN, ["props"]],
    ["heading", HEADING_PATTERN, ["props"]],
    ["image", IMAGE_PATTERN, ["props"]],
    ["svg", SVG_PATTERN, ["props"]],
    ["unordered list", UNORDERED_LIST_PATTERN, ["props"]],
    ["ordered list", ORDERED_LIST_PATTERN, ["props"]],
    ["paragraph", PARAGRAPH_PATTERN, ["props", "content"]], # paragraph pattern must go last
]

# compile PATTERNS
for p in BLOCK_PATTERNS:
    pattern = p[1]
    p[1] = re.compile(pattern, re.MULTILINE | re.DOTALL)
