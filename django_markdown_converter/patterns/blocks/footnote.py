from textwrap import dedent

from django_markdown_converter.patterns.classes.base import BasePattern


class FootnotePattern(BasePattern):
    """
    props:
    - index
    """
    def get_data(self) -> dict:
        #data = self.match.group("data").split("\n")
        #data = [_.lstrip(" ") for _ in data]
        return dedent(self.match.group("data"))
    