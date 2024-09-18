from django_markdown_converter.patterns.lookups import PATTERN_LIST, PATTERN_LOOKUP


def Revert(blocks:list=[]) -> str:
    """
    receive a list of blocks that represent
    string in markdown formatting
    converting the blocks into markdown
    return the blocks as the markdown string form
    """
    stringlist = []
    for block in blocks:
        print(f"type {block['type']}")
        current_block = PATTERN_LOOKUP[block["type"]].revert(block)
        stringlist.append(current_block)
    
    return "\n".join(stringlist)

