from django_markdown_converter.patterns.classes.base import BasePattern


class AdmonitionPattern(BasePattern):
    """
    props:
    - type
    - title
    """
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            data = m.group("data").split("\n")
            data = [_.lstrip(" ") for _ in data]
            block["data"] = "\n".join(data)
            
            self.update_props(block, m)
        return block