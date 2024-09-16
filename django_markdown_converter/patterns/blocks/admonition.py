from django_markdown_converter.patterns.classes.base import BasePattern


class AdmonitionPattern(BasePattern):
    """
    props:
    - type
    - title
    """
    def get_data(self) -> dict:
        data = self.match.group("data").split("\n")
        data = [_.lstrip(" ") for _ in data]
        return "\n".join(data)