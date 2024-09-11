from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import DEFINITIONLIST_BLOCK_DATA

'''
list_ul_processor
'''

class DefinitionListBlockifier(BaseBlockifier):
    """ Process dlist blocks """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**DEFINITIONLIST_BLOCK_DATA)
    
    def get_data(self, match, *args, **kwargs):
        return match.groupdict()
    
    def get_props(self, match, *args, **kwargs):
        return {}