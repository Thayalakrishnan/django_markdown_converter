# %%
import re

"""
ATTRS_PATTERN = r'(?:^\{(?P<props>.*?)\})?'
ATTRS_PATTERN = r'(?:^\s*\{(?P<props>.*?)\})?'
PADDED_CONTENT = r'(?P<content>(?: {1,}.*(?:\n|$))+)'
"""

ORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
PARAGRAPH_PATTERN_RAW = r'(?P<content>.*?)(?:\n|\n\n|$)' # one shot

## findall
UNORDERED_LIST_PATTERN_RAW = r'(?:^ *- (?P<item>.*?)\n)' # findall
UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(?:^ *- .*?\n)+)' # match

BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?<=^\> ).*?(?=\n|$))' # findall
BLOCKQUOTE_PATTERN_RAW = r'(?P<content>(?:^\> .*?\n)+)' # match

## header body
TABLE_PATTERN_RAW = r'(?P<header>^\|.*?\|\n)(?P<break>^\|.*?\|\n)(?P<body>(?:^\|.*?\|\n){1,})(?:\{(?P<props>.*?)\})?'
DEFINITIONLIST_PATTERN_RAW = r'(?P<term>.+?)\n(?P<definition>(?:\:\s+.*?\n)+)(?:^\{(?P<props>.*?)\})?'

## capture and dedent
FOOTNOTE_PATTERN_RAW = r'^\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)'
ADMONITION_PATTERN_RAW = r'(?:^!!!\s+(?P<type>\S+)?\s*(?:["\'](?P<title>[^"\']+?)["\'])?\s*\n)(?P<content>(?:^ {4,}.*?(?:\n|$))+)'

## two step
META_PATTERN_RAW = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'
CODE_PATTERN_RAW = r'(?:^```(?P<language>\S+)\s*\n)(?P<content>(?:^.*?\n)+)(?:^```.*?\n)(?:\{(?P<props>.*?)\})?'

## one shot
HR_PATTERN_RAW = r'^(?P<content>[\*\-]{3,})\s*(?:\s*?\{(?P<props>.*?)\})?(?:\n|$)'
IMAGE_PATTERN_RAW = r'^\!\[(?P<alt>.*?)\]\((?P<src>\S*?)\s(?P<title>.*?)?\)(?:\s*?\{(?P<props>.*?)\})?'
HEADING_PATTERN_RAW = r'^(?P<level>\#{1,})\s+(?P<content>.*?)(?:\s*?\{(?P<props>.*?)\})?(?:$|\n)'
SVG_PATTERN_RAW = r'^<svg\s(?P<attrs>[^>]*)>(?P<content>.*?)</svg>(?:\s*?\{(?P<props>.*?)\})?'

# %%
import re
"""
^ *?- .*?(?=( *?- )|(^\n)|($\n))
^ *?- (.*?)(?=(?:^ *?- )|(?:\n*$))
 *?- (.*?)(?=(?: *?- )|(?:\n*$)) # workds with flags re.DOTALL only
 ^ *?- (.*?)(?=(?:^ *?- )|(?:\n*$))
"""
ORDERED_LIST_PATTERN_RAW = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(?:^ {2,}- .*?(?=^ {2,}- ))+)(?:^\{(?P<props>.*?)\})?'

UNORDERED_LIST_PATTERN_RAW = r'(?P<content>(^ *- .*(?:(?=^ *- )|(?=^\n)|(?=$\n)))+)'
PATTERN = re.compile(UNORDERED_LIST_PATTERN_RAW, re.MULTILINE | re.DOTALL)

input_content = """- item 1
- item 2
  
  yeet
- item 3

"""

match = PATTERN.match(input_content)

if match:
    print(match.groupdict())
    #print(match)
else:
    print("no match")


# %%
import re
LIST_PATTERN_RAW = r'^ *- '
PATTERN = re.compile(LIST_PATTERN_RAW, re.MULTILINE | re.DOTALL)
input_content = """- item 1
- item 2
  
  yeet
- item 3

fdfdfefe
"""

items = re.split(PATTERN, input_content)
if items:
    print(items)
    
# %%
## findall
import re

PATTERN_RAW = r'(?:^ *?- .*?\n)(?:^ {2}.*?\n)*(?!\n^ *?- )'
PATTERN_RAW = r'(?:(?<=^- ).*?\n)(?:^ {2}.*?\n)*(?!\n^- )'
PATTERN_RAW = r'(?:(?<=^- ).*?\n)(?:(?<=^ {2}).*?\n)*(?!\n^- )'
PATTERN = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)

input_content = """- item 1
- item 2
  
  yeet
- item 3
"""

match = PATTERN.findall(input_content)

if items:
    #print(match.groupdict())
    print(match)
    print(len(match))
else:
    print("no items")
# %%
