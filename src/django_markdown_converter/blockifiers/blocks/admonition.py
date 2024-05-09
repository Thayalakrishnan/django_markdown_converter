import re
from .base import BaseBlockifier
from textwrap import dedent
'''
admonition_processor
'''

class AdmonitionBlockifier(BaseBlockifier):
    """ Process admonition blocks """
    

    def getData(self, match, *args, **kwargs):
        if match.group('content'):
            content = match.group('content')
            return dedent(content)
        return ""
        
    def getProps(self, match, *args, **kwargs):
        return {
            "type": self.get_matched_group(match, "type", ""),
            "title": self.get_matched_group(match, "title", "")
        }
    