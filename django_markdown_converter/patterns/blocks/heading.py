from django_markdown_converter.patterns.classes.base import BasePattern


class HeadingPattern(BasePattern):
    """
    heading
    """
    
    def update_props(self):
        super().update_props()
        self.block["props"]["level"] = len(self.block["props"]["level"])

