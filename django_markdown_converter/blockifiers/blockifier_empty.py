import re
from blockifiers.base_blockifier import BaseBlockifier

"""
blockifier_empty
"""
class EmptyBlockifier(BaseBlockifier):
    """ Process empty blocks. """
    
    def createBlock(self, *args, **kwargs):
        return {}