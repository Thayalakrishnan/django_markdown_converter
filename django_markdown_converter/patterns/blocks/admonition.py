from textwrap import dedent
from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.data import ADMONITION_PATTERN

class AdmonitionPattern(Pattern):
    """
    props:
    - type
    - title
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="admonition", pattern_object=ADMONITION_PATTERN, *args, **kwargs)

    def get_data(self) -> dict:
        return dedent(self.match.group("data"))
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        props = self.block.get("props", {})
        data = self.block.get("data", "")
        
        header = ["!!!"]
        atype = props.get("type", "")
        if atype:
            header.append(atype)

        title = props.get("title", "")
        if title:
            header.append(f"\"{title}\"")
            
        data = [f"    {_}" for _ in data.splitlines()]
        
        ret = []
        ret.append(" ".join(header))
        ret.extend(data)
        return "\n".join(ret)