from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import HR_PATTERN


class HRPattern(BasePattern):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("hr", HR_PATTERN, *args, **kwargs)
        
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        data = self.block.get("data", "---")
        ret = []
        ret.append(data)
        #ret.append("")
        return "\n".join(ret)