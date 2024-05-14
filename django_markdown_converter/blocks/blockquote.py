# blockquote blockifier
from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import BLOCKQUOTE_BLOCK_DATA

'''
blockifier_blockquote
cite 
'''

class BlockquoteBlockifier(BaseBlockifier):
    """ Process blockquotes """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**BLOCKQUOTE_BLOCK_DATA)

    def get_data(self, match, *args, **kwargs):
        if match.group('content'):
            content_lines = match.group('content').split("\n")
            content = [_[2:] for _ in content_lines]
            return "\n".join(content)
        return ""
 