from django_markdown_converter.patterns.classes.base import BasePattern


class DListPattern(BasePattern):
    """
    props:
    - index
    """
    def get_data(self) -> dict:
        definition = self.match.group("definition").split("\n")
        definition = [_.lstrip(": ") for _ in definition]
        definition = [_ for _ in definition if len(_)]
        term = self.match.group("term").strip("\n ")
        return {
            "term": term,
            "definition": definition,
        }
