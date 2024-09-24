from django_markdown_converter.patterns.classes.base import BasePattern


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
        current_block = BasePattern.BLOCK_LOOKUP[block["type"]].revert(block)
        stringlist.append(current_block)
    
    return "\n".join(stringlist)

