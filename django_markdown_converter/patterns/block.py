import re

"""
BLOCKQUOTE_BLOCK_DATA: ^(?P<content>(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<between>(?:\>\s+.*(?:\n|$))+))
BLOCKQUOTE_BLOCK_DATA: (?:^>\s+.*?$){1,}(?:\n\n|\n$)
"""


META_BLOCK_DATA = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'
DEFINITIONLIST_BLOCK_DATA = r'(?P<content>\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$))'
FOOTNOTE_BLOCK_DATA = r'(?P<content>\[\^(?P<index>.+?)\]:\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'

ADMONITION_BLOCK_DATA = r'(?P<content>!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'

CODE_BLOCK_DATA = r'(?P<content>(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<between>.*?)(?<=\n)(?P<stop>(?:```))\s*)'
CODE_BLOCK_DATA = r'^(?:```\s*)(?:\{(?P<attrs>.*?)\})?\n(?P<content>.*?)(?:```\s*?)$'

HR_BLOCK_DATA = r'^(?P<content>[\*\-]{3,})\s*(?:\n|$)'
TABLE_BLOCK_DATA = r'^(?P<content>(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<between>(?:.*(?:\|\n|\|$))+)(?:(?:\{\s*(?P<attrs>.*?)\s*\})?))'

TABLE_BLOCK_DATA = r'(?P<content>(?:^\|.*?\|\n){1,}(?:\{.*?\})?)'
TABLE_BLOCK_DATA = r'^(?P<header>\|.*?\|\n)(?P<break>\|.*?\|\n)(?P<content>\|.*?\|(\n|$)){1,}(?:\{(?P<attrs>.*?)\})?'


BLOCKQUOTE_BLOCK_DATA = r'(?P<content>(?:\>.*)(?:\n\>.*){1,})(?:\{(?P<attrs>.*?)\})?'
HEADING_BLOCK_DATA = r'^(?P<content>(?P<level>\#{1,6})\s+(?P<text>.*?)(?:\{(?P<attrs>.*?)\})?\s*)(?:\n|$)'
IMAGE_BLOCK_DATA = r'(?P<content>!\[(?P<attrs>.*?)\]\((?P<src>.*?)\))'
SVG_BLOCK_DATA = r'(?P<content><svg\s(?P<attrs>[^>]*)>(?P<between>.*?)</svg>)'
ORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*-\s.*?\n){1,})'
PARAGRAPH_BLOCK_DATA = r'(?P<content>.*?)(?:\n|\n\n|$)'

# other patterns
AATRS_AT_BLOCK_END = r'(?:\{(?P<attrs>.*?)\})?'
NEWLINE_REPLACE = re.compile(r'^\n{2,}', re.MULTILINE | re.DOTALL)

"""
"", 
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
