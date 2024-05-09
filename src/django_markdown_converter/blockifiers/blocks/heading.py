import re
from .base import BaseBlockifier

class HeadingBlockifier(BaseBlockifier):
    """ Process Hash Headers. """
    __slots__ = ("header", "level",)
    
    def getProps(self, match, *args, **kwargs):
        self.header = self.get_matched_group(match, "content", "").strip()
        self.level = len(match.group('level'))
        #self.tag = f"h{self.level}"
        return {
            "level": self.level,
            "id": self.header.lower().replace(" ", "-")
        }
        
    def getData(self, *args, **kwargs):
        return self.header