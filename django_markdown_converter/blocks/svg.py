from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import SVG_BLOCK_DATA

class SVGBlockifier(BaseBlockifier):
    """ Process svg blocks """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**SVG_BLOCK_DATA)
