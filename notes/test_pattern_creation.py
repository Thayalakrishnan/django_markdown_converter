import re
from django_markdown_converter.helpers.helpers import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content, extract_props
from django_markdown_converter.helpers.parsers import block_parser
from django_markdown_converter.patterns.block import BLOCK_PATTERNS, BLOCK_PATTERN

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""

TABLE_PATTERN = r'(?:^\|.*?\|\n){1,}'
ATTRS_PATTERN = r'(?:\{.*?\})?'
LAM_CONTENT_WRAPPER = lambda pat: f'(?P<content>{pat}{ATTRS_PATTERN})'

PATTERN = re.compile(LAM_CONTENT_WRAPPER(TABLE_PATTERN), re.MULTILINE | re.DOTALL)

input_content = """| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |
{ id="small-table" caption="small table of values" }
"""


match = PATTERN.match(input_content)

if match:
    print(match.groups())
