from django_markdown_converter.patterns.classes.base import BasePattern


class BlockquotePattern(BasePattern):
    """
    blockquote
    """
    def get_match(self, content):
        self.match = self.pattern.findall(content)
        
    def get_data(self) -> dict:
        lines = [_.lstrip(" ") for _ in self.match]
        return "".join(lines)