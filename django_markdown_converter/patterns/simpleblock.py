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
UNORDERED_LIST_PATTERN = r'(?:^ *- +.*$)+'

"""
#["label", pattern, ["props"]],
"""
BLOCK_PATTERNS = [
    #["meta", META_PATTERN, ["content"]],
    ["definition list", DEFINITIONLIST_PATTERN, ["term", "definition", "attrs"]],
    ["footnote", FOOTNOTE_PATTERN, ["index", "content", "attrs"]],
    ["admonition", ADMONITION_PATTERN, ["attrs"]],
    ["code", CODE_PATTERN, ["attrs"]],
    ["table", TABLE_PATTERN, ["header", "body", "break", "attrs"]],
    ["blockquote", BLOCKQUOTE_PATTERN, ["attrs"]],
    ["hr", HR_PATTERN, ["attrs"]],
    ["heading", HEADING_PATTERN, ["attrs"]],
    ["image", IMAGE_PATTERN, ["attrs"]],
    ["svg", SVG_PATTERN, ["attrs"]],
    ["unordered list", UNORDERED_LIST_PATTERN, ["attrs"]],
    ["ordered list", ORDERED_LIST_PATTERN, ["attrs"]],
    ["paragraph", PARAGRAPH_PATTERN, ["attrs", "content"]], # paragraph pattern must go last
]

# compile PATTERNS
for p in BLOCK_PATTERNS:
    pattern = p[1]
    p[1] = re.compile(pattern, re.MULTILINE | re.DOTALL)
