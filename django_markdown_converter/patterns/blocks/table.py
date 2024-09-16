from django_markdown_converter.patterns.classes.base import BasePattern


class TablePattern(BasePattern):
    """
    props:
    - header
    - body
    """
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            block["data"] = {
                "header": get_row(m.group("header")),
                "body": get_rows(m.group("body")),
            }
        return block
    
    
    
def get_row(line:str="") -> list:
    """strip leading and trailing pipes,"""
    line = line.strip("|\n ")
    return [_.strip() for _ in line.split("|")]
    
def get_rows(chunk:str="")-> list:
    lines = chunk.split("\n")
    return [get_row(line) for line in lines if len(line)]