import re
from django_markdown_converter.helpers.helpers import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content, extract_attrs
from django_markdown_converter.helpers.parsers import block_parser
from django_markdown_converter.patterns.block import BLOCK_PATTERNS, BLOCK_PATTERN

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
    #print(f"{index} ----- {label}")
    #print(f"---------------")
    pass


"""
loop over the content and spit out chunks

match = BLOCK_PATTERN.finditer(raw_chunk)
expected = []
for index, m in enumerate(match):
    chunk = m.group("block")
    current_block = []
    # determine the type of block each chunk is
    for label, pattern, items, contains_attrs in BLOCK_PATTERNS:
        submatch = pattern.match(chunk)
        if submatch:
            current_block.append(index)
            current_block.append(label)
            content = submatch.group("content")
            # check the content for attributes
            if contains_attrs:
                content, attrs = extract_attrs(content)
                current_block.append(content)
                current_block.append(attrs)
            else:
                current_block.append(content)
                current_block.append(False)
            break

    expected.append(current_block)

for i in expected:
    print(i)
"""