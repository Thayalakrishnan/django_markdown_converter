from textwrap import dedent

from django_markdown_converter.patterns.classes.base import BasePattern


class FootnotePattern(BasePattern):
    """
    props:
    - index
    """
    def get_data(self) -> dict:
        return dedent(self.match.group("data"))
    
    def revert(self, *args, **kwargs) -> str:
        block = super().revert(*args, **kwargs)
        
        props = block.get("props", {})
        index = props.get("index", 1)
        
        data = block.get("data", "")
        data = [f"    {_}" for _ in data.splitlines()]
        
        ret = []
        ret.append(f"[^{index}]:")
        ret.extend(data)
        ret.append(f"")
        return "\n".join(ret)