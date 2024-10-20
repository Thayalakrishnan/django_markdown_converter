import re
from django_markdown_converter.patterns.classes.base import Pattern


EMPTY_PATTERN = {
    "type": "empty",
    "check": r'.*',
    "pattern": r'(?P<data>.*)',
    "flags": re.MULTILINE | re.DOTALL,
    "addToLookup": False,
    "hasNested": False,
    "hasInlineMarkup": False,
    "props": [],
    "data": ["data"],
}

class EmptyPattern(Pattern):
    """
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("empty", EMPTY_PATTERN, *args, **kwargs)

    #def convert(self, *args, **kwargs) -> str:
    #    return ""
    #def revert(self, *args, **kwargs) -> str:
    #    return ""
    
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        return super().convert(content, props, *args, **kwargs)
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        return super().revert(*args, **kwargs)