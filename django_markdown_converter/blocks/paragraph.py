# paragraph_processor
#from django_markdown_converter.blocks.base import BaseBlockifier
#from ...inlineifiers.inline_parser import InlineParser
#from ..blockifier_data import PARAGRAPH_BLOCK_DATA

from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import PARAGRAPH_BLOCK_DATA
from django_markdown_converter.inlineifiers.new_inline_parser import InlineParser

'''
need to be mindful that a paragraph block may also, unwittingly
contain a list block within it due to not leaving enough space
so we need to check for that when we parse the paragraphs line by line
'''

class ParagraphBlockifier(BaseBlockifier):
    """ Process paragraphs """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**PARAGRAPH_BLOCK_DATA)
    
    def blockify(self, lines:list=[]):
        
        p_blocks = []
        for p in lines:
            p = p.strip()
            if len(p):
                block = self.create_block(chunk=p, lines=lines)
                p_blocks.append(block)
                
        #print(f"blockify paragraph")
        #if len(p_blocks) > 1:
        #    print("blocks")
        #    for b in p_blocks:
        #        print(b)
        
        if len(p_blocks):
            return p_blocks
        return {}
    
    def get_data(self, chunk, *args, **kwargs):
        #print("get data")
        #print(repr(chunk))
        #print(InlineParser(chunk))
        return InlineParser(chunk)
        #return "".join(InlineParser([chunk]))
    
    def get_props(self, *args, **kwargs):
        return {}
        
 