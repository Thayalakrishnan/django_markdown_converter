from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.inlines.parser import inline_parser


class TablePattern(BasePattern):
    """
    props:
    - header
    - body
    """
    def get_data(self) -> dict:
        return {
            "header": get_row(self.match.group("header")),
            "body": get_rows(self.match.group("body")),
        }
    
    
def get_row(line:str="") -> list:
    """strip leading and trailing pipes,"""
    line = line.strip("|\n ")
    return [inline_parser(_.strip()) for _ in line.split("|")]
    
def get_rows(chunk:str="")-> list:
    lines = chunk.split("\n")
    return [get_row(line) for line in lines if len(line)]