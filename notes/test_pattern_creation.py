# %%
import re

META_PATTERN_RAW = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'


ORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'

PARAGRAPH_PATTERN_RAW = r'(?P<content>.*?)(?:\n|\n\n|$)'

ATTRS_PATTERN = r'(?:^\{(?P<props>.*?)\})?'
ATTRS_PATTERN = r'(?:^\s*\{(?P<props>.*?)\})?'
PADDED_CONTENT = r'(?P<content>(?: {1,}.*(?:\n|$))+)'

UNORDERED_LIST_PATTERN_RAW = r'(?:^ *- (?P<item>.*?)\n)' # findall
UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(?:^ *- .*?\n)+)' # match

BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?<=^\> ).*?(?=\n|$))' # findall
BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?:^\> .*?\n)+)' # match

ADMONITION_PATTERN_RAW = r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<content>(?:^ {4,}.*?(?:\n|$))+)'
HR_PATTERN_RAW = r'^(?P<content>[\*\-]{3,})\s*(?:\s*?\{(?P<props>.*?)\})?(?:\n|$)'
HEADING_PATTERN_RAW = r'^(?P<level>\#{1,})\s+(?P<content>.*?)(?:\s*?\{(?P<props>.*?)\})?(?:$|\n)'
IMAGE_PATTERN_RAW = r'^\!\[(?P<alt>.*?)\]\((?P<src>\S*?)\s(?P<title>.*?)?\)(?:\s*?\{(?P<props>.*?)\})?'
SVG_PATTERN_RAW = r'^<svg\s(?P<attrs>[^>]*)>(?P<content>.*?)</svg>(?:\s*?\{(?P<props>.*?)\})?'
CODE_PATTERN_RAW = r'(?:^```(?P<language>\S+)\s*\n)(?P<content>(?:^.*?\n)+)(?:^```.*?\n)(?:\{(?P<props>.*?)\})?'
TABLE_PATTERN_RAW = r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})(?:\{(?P<props>.*?)\})?'
FOOTNOTE_PATTERN_RAW = r'^\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)'
DEFINITIONLIST_PATTERN_RAW = r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?\n)+)(?:^\{(?P<props>.*?)\})?'

# %%
import re

ORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(?:^ *- .*?(?=^ *-|$|^\n))+)(?:^\{(?P<props>.*?)\})?'
PATTERN = re.compile(UNORDERED_LIST_PATTERN_RAW, re.MULTILINE | re.DOTALL)

input_content = """- item 1
- item 2
  
  yeet
- item 3
{ type="ulist" }
"""

match = PATTERN.match(input_content)

if match:
    print(match.groupdict())
    #print(match)
else:
    print("no match")


# %%
