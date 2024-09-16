from django_markdown_converter.patterns.classes.base import BasePattern


class BlockquotePattern(BasePattern):
    """
    blockquote
    """
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.findall(content)
        if m:
            m = [_.lstrip(" ") for _ in m]
            block["data"] = "".join(m)
        return block
