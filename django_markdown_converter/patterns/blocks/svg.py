from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import SVG_PATTERN


class SVGPattern(BasePattern):
    """
    svg elements
    props:
    - attrs
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("svg", SVG_PATTERN, *args, **kwargs)

    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        generate_attrs = lambda k,v: f'{k}="{v}"'
        pad_if_present = lambda x: f' {x}' if len(x) else f''
        wrap_html_content = lambda t, a, c: f'<{t}{pad_if_present(a)}>{c}</{t}>'
        
        props = self.block.get("props", {})
        attrs = " ".join(list(map(generate_attrs, zip(props.keys(), props.values()))))
        
        data = self.block.get("data", "")
        
        ret = []
        ret.append(wrap_html_content("svg", attrs, data))
        ret.append("")
        return "\n".join(ret)