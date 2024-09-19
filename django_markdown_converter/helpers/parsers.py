from django_markdown_converter.patterns.generic import BLOCK_PATTERN
from django_markdown_converter.helpers.processors import excise_props, process_input_content
from django_markdown_converter.patterns.lookups import PATTERN_LIST, PATTERN_LOOKUP


def block_generator(content:str=""):
    """
    generator function that loops over the content 
    and yields blocks according to the block pattern
    """
    chunks = BLOCK_PATTERN.finditer(content)
    for index, chunk in enumerate(chunks):
        block = chunk.group("block")
        props = chunk.group("props")
        if block:
            yield block, props, index


def block_detector(block:str="", props:str="", index:int=0) -> dict:
    """
    receives a 'block' and determinest the type
    of block content using the block patterns list. 
    """
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
    for block, props, index in blocks:
        yield block_detector(block, props, index)
    
    
def nested_blocks_parser() -> bool:
    """
    """
    content_was_processed = False
    for pattern in PATTERN_LIST:
        if pattern.hasNested:
            ## loop over our patterns whicvh 
            ## may have nested content
            for _ in pattern.bank:
                ## if the content is already formated skip it
                if isinstance(_["data"], list):
                    continue  
                
                ## convert the content into blocks
                newdata = list(block_parser(process_input_content(_["data"])))
                
                #if pattern.blocktype == "olist" or pattern.blocktype == "ulist":
                #    if len(newdata) == 1:
                
                if len(newdata):
                    _["data"] = newdata
                    content_was_processed = True
    return content_was_processed
