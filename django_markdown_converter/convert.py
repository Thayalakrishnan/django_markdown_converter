from django_markdown_converter.patterns.classes.base import BasePattern, process_input_content


def Convert(source:str="") -> list:
    """
    receive a string, presumably formatted
    using markdown
    convert the markdown into our json format
    and return this object
    """
    blocks = []
    source = process_input_content(source)
    for block in BasePattern.block_parser(source):
        blocks.append(block)
    while BasePattern.nested_blocks_parser():
        continue
    return blocks
