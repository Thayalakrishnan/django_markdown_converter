from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import HR_BLOCK_DATA

class HRBlockifier(BaseBlockifier):
    
    def __init__(self, *args, **kwargs) -> None:
            super().__init__(**HR_BLOCK_DATA)
    """ Process Horizontal Rules. """
    def get_props(self, *args, **kwargs):
        return {}
    
    def get_data(self, *args, **kwargs):
        return " "

