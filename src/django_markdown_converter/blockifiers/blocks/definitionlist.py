import re
from .base import BaseBlockifier
#from blockify import Blockify

'''
list_ul_processor
'''

class DefinitionListBlockifier(BaseBlockifier):
    """ Process definition list blocks """
    
    def getData(self, match, *args, **kwargs):
        return match.groupdict()
    
    def getProps(self, match, *args, **kwargs):
        return {}