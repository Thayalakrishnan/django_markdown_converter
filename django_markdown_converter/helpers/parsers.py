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
        #block =  remove_trailing_whitespace(block)
        yield block, index


def block_detector(block:str="", index:int=0):
    """
    receives a 'block' and determinest the type
    of block content using the block patterns list. 
    """
    # determine the type of block each chunk is
    attrs = ""
    # extract any attrs that are in this block
    block, attrs = extract_attrs(block)
    
    for label, pattern, props in BLOCK_PATTERNS:
        submatch = pattern.match(block)
        if submatch:
            #content = submatch.group("content")
            content = submatch.group(0)
            #if block != content:
            #    print("bad match")
            #    continue
            # check the content for attributes
            if attrs:
                #print(f"---------------------------------------------\n")
                print(f"{index} | {repr(attrs)} |")
                #print(content)
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
    