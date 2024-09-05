import re

"""
BLOCKQUOTE_BLOCK_DATA: ^(?P<content>(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<between>(?:\>\s+.*(?:\n|$))+))
BLOCKQUOTE_BLOCK_DATA: (?:^>\s+.*?$){1,}(?:\n\n|\n$)
"""


META_PATTERN = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'
DEFINITIONLIST_PATTERN = r'(?P<content>\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$))'
FOOTNOTE_PATTERN = r'(?P<content>\[\^(?P<index>.+?)\]:\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'

ADMONITION_PATTERN = r'(?P<content>!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'

CODE_PATTERN = r'(?P<content>(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<between>.*?)(?<=\n)(?P<stop>(?:```))\s*)'
CODE_PATTERN = r'^(?:```\s*)(?:\{(?P<attrs>.*?)\})?\n(?P<content>.*?)(?:```\s*?)$'


HR_PATTERN = r'^(?:[\*\-]{3,} *(?:\s?\{.*?\})?$)' # multiline
TABLE_PATTERN = r'(?:^\|.*?\| *?$\n)+(?:\{.*?\})?' # multiline
BLOCKQUOTE_PATTERN = r'(?:^> *?.*?$\n)+(?:\{.*?\})?' # multiline
HEADING_PATTERN = r'^\#+\s+.*?$' # multiline
IMAGE_PATTERN = r'^!\[.*?\]\(.*?\)' # multiline, dotall
SVG_PATTERN = r'^<svg\s(?P<attrs>[^>]*)>(?P<between>.*?)</svg>' # multiline, dotall
ORDERED_LIST_PATTERN = r'(?:^ *[\-\*\+] +.*?\n)+(?=\n)' # multiline, dotall
UNORDERED_LIST_PATTERN = r'(^ *\d+\. +.*?$\n)+(?=\n)' # multiline, dotall
PARAGRAPH_PATTERN = r'(?:.*?)(?:\n|\n\n|$)' # multiline, dotall







"""
"""
BLOCK_PATTERNS = [
    ["meta", META_BLOCK_DATA, ["content"], False],
    ["definition list", DEFINITIONLIST_BLOCK_DATA, ["term", "definition", "attrs"], True],
    ["footnote", FOOTNOTE_BLOCK_DATA, ["index", "content", "attrs"], True],
    ["admonition", ADMONITION_BLOCK_DATA, ["attrs"], True],
    ["code", CODE_BLOCK_DATA, ["attrs"], True],
    ["table", TABLE_BLOCK_DATA, ["header", "body", "break", "attrs"], True],
    ["blockquote", BLOCKQUOTE_BLOCK_DATA, ["attrs"], True],
    ["hr", HR_BLOCK_DATA, ["attrs"], True],
    ["heading", HEADING_BLOCK_DATA, ["attrs"], True],
    ["image", IMAGE_BLOCK_DATA, ["attrs"], True],
    ["svg", SVG_BLOCK_DATA, ["attrs"], True],
    ["unordered list", UNORDERED_LIST_BLOCK_DATA, ["attrs"], True],
    ["ordered list", ORDERED_LIST_BLOCK_DATA, ["attrs"], True],
    ["paragraph", PARAGRAPH_BLOCK_DATA, ["attrs", "content"], True],
]

# compile PATTERNS
for p in BLOCK_PATTERNS:
    p[1] = re.compile(p[1], re.MULTILINE | re.DOTALL)
    
# generic block level element
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n\n'
BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)
