from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import IMAGE_BLOCK_DATA

class ImageBlockifier(BaseBlockifier):
    """ Process image blocks """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**IMAGE_BLOCK_DATA)
    