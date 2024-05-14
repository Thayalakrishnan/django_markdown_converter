from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import ADMONITION_BLOCK_DATA

from textwrap import dedent
'''
admonition_processor
'''

class AdmonitionBlockifier(BaseBlockifier):
    """ Process admonition blocks """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**ADMONITION_BLOCK_DATA)

    def get_data(self, match, *args, **kwargs):
        if match.group('content'):
            content = match.group('content')
            return dedent(content)
        return ""
        
    def get_props(self, match, *args, **kwargs):
        return {
            "type": self.get_matched_group(match, "type", ""),
            "title": self.get_matched_group(match, "title", "")
        }
    