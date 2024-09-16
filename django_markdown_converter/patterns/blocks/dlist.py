from django_markdown_converter.patterns.classes.base import BasePattern


class DListPattern(BasePattern):
    """
    props:
    - index
    """
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            block["data"] = m.groupdict()
            definition = m.group("definition").split("\n")
            definition = [_.lstrip(": ") for _ in definition]
            block["data"]["definition"] = definition
        return block
    