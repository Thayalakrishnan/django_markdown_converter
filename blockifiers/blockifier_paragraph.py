# paragraph_processor
from blockifiers.base_blockifier import BaseBlockifier
from inlineifiers.inline_parser import InlineParser

'''
need to be mindful that a paragraph block may also, unwittingly
contain a list block within it due to not leaving enough space
so we need to check for that when we parse the paragraphs line by line
'''

class ParagraphBlockifier(BaseBlockifier):
    """ Process paragraphs """
    
    def blockify(self, lines:list=[]):
        p_blocks = []
        for p in lines:
            p = p.strip()
            if len(p):
                block = self.createBlock(chunk=p, lines=lines)
                p_blocks.append(block)

        if len(p_blocks):
            return p_blocks
        return {}
    
    def getData(self, chunk, *args, **kwargs):
        return "".join(InlineParser([chunk]))
    
    def getProperties(self, *args, **kwargs):
        return {}
        
 