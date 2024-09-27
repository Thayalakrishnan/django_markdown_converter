from django_markdown_converter.patterns.classes.base import BasePattern, process_input_content


def Convert(source:str="") -> list:
    """
    receive a string, presumably formatted
    using markdown
    convert the markdown into our json format
    and return this object
    """
    bp = BasePattern()
    return bp.convert_md_to_json(source)
