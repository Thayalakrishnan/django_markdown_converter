from django_markdown_converter.blocks.base import BaseBlockifier


"""
blockifier_empty
"""
class EmptyBlockifier(BaseBlockifier):
    """ Process empty blocks. """
    
    def createBlock(self, *args, **kwargs):
        return {}