import re

"""
"""

#TABLE_PATTERN = (r'(?:^\|.*?\|$(?:\n|$))+(?:\{.*?\})?', re.MULTILINE)
#HR_PATTERN = (r'^(?:[\*\-]{3,}$)', re.MULTILINE)
#CODE_PATTERN = (r'(?:^```.*?$\n)(?:.*?$\n)+?(?:^```)', re.MULTILINE)

META_PATTERN = r'^---.*?^---$'
CODE_PATTERN = r'^```.*?^```$'
DEFINITIONLIST_PATTERN = r'^.+?$\n(?:\: .*$)'
FOOTNOTE_PATTERN = r'^\[\^\d+\]\:\n.*$'
ADMONITION_PATTERN = r'(?:^!!!.*$)'
TABLE_PATTERN = r'(?:^\|.*?\|\s*?$\n?)+'
HR_PATTERN = r'^(?:[\*\-]{3,}$)'
HEADING_PATTERN = r'^\#+\s+.*?$'
IMAGE_PATTERN = r'^!\[.*?\]\(.*?\)'
SVG_PATTERN = r'^<svg\s[^>]*>(?:.*?)</svg>'
PARAGRAPH_PATTERN = r'.*'
UNORDERED_LIST_PATTERN = r'(?:^ *- +.*$)+'
ORDERED_LIST_PATTERN = r'(?:^ *\d+\. +.*$)+'
BLOCKQUOTE_PATTERN = r'(?:^>.*$)+'

HTML_PATTERN = r'^<(?P<el>\S+)\s[^>]*>(?:.*?)</(?P=el)>'

"""
#["label", pattern],
"""
BLOCK_PATTERNS_RAW = [
    #["meta", META_PATTERN],
    ["dlist", DEFINITIONLIST_PATTERN],
    ["footnote", FOOTNOTE_PATTERN],
    ["admonition", ADMONITION_PATTERN],
    ["code", CODE_PATTERN],
    ["table", TABLE_PATTERN],
    ["blockquote", BLOCKQUOTE_PATTERN],
    ["hr", HR_PATTERN],
    ["heading", HEADING_PATTERN],
    ["image", IMAGE_PATTERN],
    ["svg", SVG_PATTERN],
    ["ulist", UNORDERED_LIST_PATTERN],
    ["olist", ORDERED_LIST_PATTERN],
    ["paragraph", PARAGRAPH_PATTERN],
]


BLOCK_PATTERNS = [(p[0], re.compile(p[1], re.MULTILINE | re.DOTALL)) for p in BLOCK_PATTERNS_RAW]
