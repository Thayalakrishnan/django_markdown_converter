from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import DEFINITIONLIST_BLOCK_DATA
#from blockify import Blockify

'''
list_ul_processor
'''

class DefinitionListBlockifier(BaseBlockifier):
    """ Process definition list blocks """
    def __init__(self, *args, **kwargs) -> None:
            super().__init__(**DEFINITIONLIST_BLOCK_DATA)
    
    def getData(self, match, *args, **kwargs):
        return match.groupdict()
    
    def getProps(self, match, *args, **kwargs):
        return {}