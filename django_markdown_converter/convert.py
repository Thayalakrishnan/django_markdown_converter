from django_markdown_converter.helpers.processors import process_input_content
from django_markdown_converter.helpers.parsers import block_parser, nested_blocks_parser


def Convert(source:str="") -> list:
    """
    receive a string, presumably formatted
    using markdown
    convert the markdown into our json format
    and return this object
    """
    blocks = []
    source = process_input_content(source)
    for block in block_parser(source):
        blocks.append(block)
    while nested_blocks_parser():
        continue
    return blocks
