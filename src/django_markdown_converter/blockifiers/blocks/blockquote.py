import re
# paragraph_processor
from .base import BaseBlockifier

'''
blockifier_blockquote
cite 
'''

class BlockquoteBlockifier(BaseBlockifier):
    """ Process blockquotes """
        
    def getData(self, match, *args, **kwargs):
        if match.group('content'):
            content_lines = match.group('content').split("\n")
            content = [_[2:] for _ in content_lines]
            return "\n".join(content)
        return ""
 