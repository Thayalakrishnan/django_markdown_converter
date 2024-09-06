#from django_markdown_converter.patterns.block import BLOCK_PATTERN, BLOCK_PATTERNS
from django_markdown_converter.patterns.block import BLOCK_PATTERN
from django_markdown_converter.patterns.simpleblock import BLOCK_PATTERNS
from django_markdown_converter.helpers.processors import extract_attrs, remove_trailing_whitespace


def block_iterator(content:str=""):
    """
    generator function that loops over the content 
    and yields blocks according to the block pattern
    """
    chunks = BLOCK_PATTERN.finditer(content)
    for index, chunk in enumerate(chunks):
        block = chunk.group("block")
        block =  remove_trailing_whitespace(block)
        yield block, index


def block_detector(block:str="", index:int=0):
    """
    receives a 'block' and determinest the type
    of block content using the block patterns list. 
    """
    # determine the type of block each chunk is
    for label, pattern, props, contains_attrs in BLOCK_PATTERNS:
        submatch = pattern.match(block)
        if submatch:
            #content = submatch.group("content")
            content = submatch.group(0)
            #if block != content:
            #    print("bad match")
            #    continue
            attrs = ""
            # check the content for attributes
            if contains_attrs:
                content, attrs = extract_attrs(block)
                if attrs:
                    print(f"{index} | {repr(attrs)}")
                else:
                    print("\nNO ATTRS DETECTED\n")
                    print(block)
            return index, label, content, attrs


def block_parser(content:str=""):
    """
    from the content, loop over it to create blocks
    return an object that indicates the blocks
    index, the type of block, the content extracted 
    and any props
    """
    blocks = block_iterator(content)
    for block, index in blocks:
        yield block_detector(block, index)
    