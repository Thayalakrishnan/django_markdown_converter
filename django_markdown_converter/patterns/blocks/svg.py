from django_markdown_converter.patterns.classes.base import BasePattern

class SVGPattern(BasePattern):
    """
    svg elements
    props:
    - attrs
    """


    def revert(self, *args, **kwargs) -> str:
        block = super().revert(*args, **kwargs)
        
        props = block.get("props", {})
        data = block.get("data", "")
        
        ret = []
        ret.append(f"")
        ret.extend(data)
        return "\n".join(ret)