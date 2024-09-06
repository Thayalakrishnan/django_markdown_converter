from django_markdown_converter.helpers.helpers import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content
from django_markdown_converter.helpers.parsers import block_parser

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""

path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)
raw_chunk = process_input_content(raw_chunk)

for index, label, content, attrs in block_parser(raw_chunk):
    pass
