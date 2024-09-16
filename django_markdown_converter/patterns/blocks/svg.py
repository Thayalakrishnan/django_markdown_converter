from django_markdown_converter.patterns.classes.base import BasePattern

class SVGPattern(BasePattern):
    """
    svg elements
    props:
    - attrs
    """
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            block["data"] = m.group("data")
            self.update_props(block, m)
        return block