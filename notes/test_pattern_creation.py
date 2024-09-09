# %%
import re

META_PATTERN_RAW = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'
DEFINITIONLIST_PATTERN_RAW = r'(?P<content>\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$))'
FOOTNOTE_PATTERN_RAW = r'(?P<content>\[\^(?P<index>.+?)\]:\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'

ORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*-\s.*?\n){1,})'
PARAGRAPH_PATTERN_RAW = r'(?P<content>.*?)(?:\n|\n\n|$)'

ATTRS_PATTERN = r'(?:\{(?P<props>.*?)\})?'
ATTRS_PATTERN = r'(?:\s*\{(?P<props>.*?)\})?'

BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?<=^\> ).*?(?=\n|$))' # this is a findall situation
BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?:^\> .*?\n)+)' # this is a match situation

ADMONITION_PATTERN_RAW = r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<content>(?: {1,}.*(?:\n|$)))+'

HR_PATTERN_RAW = r'^(?P<content>[\*\-]{3,})\s*(?:\s*?\{(?P<props>.*?)\})?(?:\n|$)'
HEADING_PATTERN_RAW = r'^(?P<level>\#{1,})\s+(?P<content>.*?)(?:\s*?\{(?P<props>.*?)\})?(?:$|\n)'
IMAGE_PATTERN_RAW = r'^\!\[(?P<alt>.*?)\]\((?P<src>\S*?)\s(?P<title>.*?)?\)(?:\s*?\{(?P<props>.*?)\})?'
SVG_PATTERN_RAW = r'^<svg\s(?P<attrs>[^>]*)>(?P<content>.*?)</svg>(?:\s*?\{(?P<props>.*?)\})?'
CODE_PATTERN_RAW = r'(?:^```(?P<language>\S+)\s*\n)(?P<content>(?:^.*?\n)+)(?:^```.*?\n)(?:\{(?P<props>.*?)\})?'
TABLE_PATTERN_RAW = r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})(?:\{(?P<props>.*?)\})?'

PATTERN = re.compile(ADMONITION_PATTERN_RAW, re.MULTILINE | re.DOTALL)


input_content = """!!! note "Note Title"
    line 1.
    line 2.
"""

match = PATTERN.match(input_content)

if match:
    print(match.groupdict())
    #print(match)


# %%
