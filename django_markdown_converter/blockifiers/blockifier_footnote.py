import re
from blockifiers.base_blockifier import BaseBlockifier

'''
blockifier_footnote
'''

class FootnoteBlockifier(BaseBlockifier):
    """ Process admonition blocks """
    
    def createBlock(self, match, *args, **kwargs):
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
            "blocktype": self.name,
            "properties": {},
            "data": self.bank
        }