from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import HEADING_BLOCK_DATA

class HeadingBlockifier(BaseBlockifier):
    """ Process Hash Headers. """
    __slots__ = ("header", "level",)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**HEADING_BLOCK_DATA)
    
    def get_props(self, match, *args, **kwargs):
        self.header = self.get_matched_group(match, "content", "").strip()
        self.level = len(match.group('level'))
        #self.tag = f"h{self.level}"
        return {
            "level": self.level,
            "id": self.header.lower().replace(" ", "-")
        }
        
    def get_data(self, *args, **kwargs):
        return self.header