from django_markdown_converter.patterns.block import BLOCK_PATTERN
from django_markdown_converter.helpers.processors import excise_props
from django_markdown_converter.patterns.procpats import PATTERN_LIST


def block_generator(content:str=""):
    """
    generator function that loops over the content 
    and yields blocks according to the block pattern
    """
    chunks = BLOCK_PATTERN.finditer(content)
    for index, chunk in enumerate(chunks):
        block = chunk.group("block")
        yield block, index


def block_detector(block:str="", index:int=0) -> dict:
    """
    receives a 'block' and determinest the type
    of block content using the block patterns list. 
    """
    # determine the type of block each chunk is
    props = ""
    # extract any props that are in this block
    block, props = excise_props(block)
    for pattern in PATTERN_LIST:
        if pattern.check(block):
            return pattern.convert(block, props)

def block_parser(content:str=""):
    """
    from the content, loop over it to create blocks
    return an object that indicates the blocks
    index, the type of block, the content extracted 
    and any props
    """
    blocks = block_generator(content)
    for block, index in blocks:
        yield block_detector(block, index)
    