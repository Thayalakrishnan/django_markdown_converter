from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.inlines.parser import convert_inline, revert_inline
from django_markdown_converter.patterns.data import PARAGRAPH_PATTERN


class ParagraphPattern(Pattern):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="paragraph", pattern_object=PARAGRAPH_PATTERN, *args, **kwargs)
        
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        super().convert(content, props, *args, **kwargs)
        self.block["data"] = convert_inline(self.block["data"])
        return self.block
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        data = self.block.get("data", "")
        return revert_inline(data)