from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.data import BLOCKQUOTE_PATTERN


class BlockquotePattern(Pattern):
    """
    blockquote
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="blockquote", pattern_object=BLOCKQUOTE_PATTERN, *args, **kwargs)
        
    #def get_match(self, content):
    #    self.match = self.pattern.findall(content)
        
    def get_data(self) -> dict:
        lines = [_.lstrip(" ") for _ in self.match]
        return "".join(lines)
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        data = self.block.get("data", "")
        data = [f"> {_}" for _ in data.splitlines()]
        
        ret = []
        ret.extend(data)
        return "\n".join(ret)