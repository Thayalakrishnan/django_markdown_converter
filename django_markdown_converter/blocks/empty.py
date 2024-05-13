from django_markdown_converter.blocks.base import BaseBlockifier


"""
blockifier_empty
"""
class EmptyBlockifier(BaseBlockifier):
    """ Process empty blocks. """
    
    def create_block(self, *args, **kwargs):
        return {}