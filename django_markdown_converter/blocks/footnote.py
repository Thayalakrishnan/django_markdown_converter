from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import FOOTNOTE_BLOCK_DATA

'''
blockifier_footnote
'''

class FootnoteBlockifier(BaseBlockifier):
    """ Process admonition blocks """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**FOOTNOTE_BLOCK_DATA)
            
    def create_block(self, match, *args, **kwargs):
        '''
        '''
        if match.group('index'):
            index = int(match.group('index'))
            
        if match.group('content'):
            content = match.group('content')
        
        block = {
            "index": index,
            "data": content + "\n"
        }
        
        self.bank.append(block)
        return {}
    
    def getFootnotes(self):
        return {
            "type": self.name,
            "props": {},
            "data": self.bank
        }