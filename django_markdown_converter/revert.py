from django_markdown_converter.patterns.classes.base import BasePattern


def Revert(blocks:list=[]) -> str:
    """
    receive a list of blocks that represent
    string in markdown formatting
    converting the blocks into markdown
    return the blocks as the markdown string form
    """
    strings = []
    bp = BasePattern()
    for string in bp.block_reverter(blocks):
        strings.append(string)
    return "\n".join(strings)

