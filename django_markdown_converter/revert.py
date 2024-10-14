from django_markdown_converter.patterns.classes.base import BasePattern


def Revert(blocks:list=[]) -> str:
    """
    receive a list of blocks that represent
    string in markdown formatting
    converting the blocks into markdown
    return the blocks as the markdown string form
    """
    bp = BasePattern()
    return bp.convert_json_to_md(blocks)
