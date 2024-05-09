from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import HR_BLOCK_DATA

class HRBlockifier(BaseBlockifier):
    
    def __init__(self, *args, **kwargs) -> None:
            super().__init__(**HR_BLOCK_DATA)
    """ Process Horizontal Rules. """
    def getProps(self, *args, **kwargs):
        return {}
    
    def getData(self, *args, **kwargs):
        return " "

