from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.inlines.parser import inline_parser

class ParagraphPattern(BasePattern):
    
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        super().convert(content, props, *args, **kwargs)
        self.block["data"] = inline_parser(self.block["data"])
        return self.block
    
    def revert(self, *args, **kwargs) -> str:
        block = super().revert(*args, **kwargs)
        data = block.get("data", "")
        ret = []
        ret.append(data)
        ret.append("")
        return "\n".join(ret)