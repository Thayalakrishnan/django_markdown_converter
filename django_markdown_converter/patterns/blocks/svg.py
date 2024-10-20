from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.data import SVG_PATTERN


class SVGPattern(Pattern):
    """
    svg elements
    props:
    - attrs
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="svg", pattern_object=SVG_PATTERN, *args, **kwargs)

    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        generate_attrs = lambda k: f'{k[0]}="{k[1]}"'
        pad_if_present = lambda x: f' {x}' if len(x) else f''
        wrap_html_content = lambda t, a, c: f'<{t}{pad_if_present(a)}>{c}</{t}>'
        
        props = self.block.get("props", {})
        print(props)
        attrs = ""
        
        if props:
            attrs = " ".join(list(map(generate_attrs, props.items())))
        
        data = self.block.get("data", "")
        ret = []
        ret.append(wrap_html_content("svg", attrs, data))
        return "\n".join(ret)