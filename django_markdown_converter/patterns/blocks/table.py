from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.inlines.parser import inline_parser
from django_markdown_converter.patterns.data import TABLE_PATTERN


class TablePattern(BasePattern):
    """
    props:
    - header
    - body
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("table", TABLE_PATTERN, *args, **kwargs)
            
    def get_data(self) -> dict:
        return {
            "header": get_row(self.match.group("header")),
            "body": get_rows(self.match.group("body")),
        }
        
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        create_row_lambda = lambda x: f"| {' | '.join(x)} |"
        
        data = self.block.get("data", "")
        
        header = data.get("header", [])
        body = data.get("body", [])
        breaker = ['---']*len(header)
        
        ret = []
        ret.append(f"")
        ret.extend(data)
        
        ret.append(create_row_lambda(header))
        ret.append(create_row_lambda(breaker))
        for row in body:
            ret.append(create_row_lambda(row))
        return "\n".join(ret)
    
    
def get_row(line:str="") -> list:
    """strip leading and trailing pipes,"""
    line = line.strip("|\n ")
    return [inline_parser(_.strip()) for _ in line.split("|")]
    
def get_rows(chunk:str="")-> list:
    lines = chunk.split("\n")
    return [get_row(line) for line in lines if len(line)]