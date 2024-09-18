from textwrap import dedent

from django_markdown_converter.patterns.classes.base import BasePattern

class AdmonitionPattern(BasePattern):
    """
    props:
    - type
    - title
    """
    def get_data(self) -> dict:
        return dedent(self.match.group("data"))
    
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        props = self.block.get("props", {})
        data = self.block.get("data", "")
        
        atype = f' {props.get("type", "")}'.rstrip()
        title = f' {props.get("title", "")}'.rstrip()

        data = [f"    {_}" for _ in data.splitlines()]
        
        ret = []
        ret.append(f"!!!{atype}{title}")
        ret.extend(data)
        ret.append(f"")
        return "\n".join(ret)