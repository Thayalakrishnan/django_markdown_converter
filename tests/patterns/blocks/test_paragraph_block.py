import pytest
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern


PARAGRAPH_BLOCK_DATA = {
    "type": "paragraph",
    "props": {},
    "data": "This is the first sentence in the paragraph."
}


PARAGRAPH_MD_DATA = f'''{PARAGRAPH_BLOCK_DATA["data"]}'''

def test_basic_conversion():
    result = ParagraphPattern().convert(PARAGRAPH_MD_DATA)
    assert PARAGRAPH_BLOCK_DATA == result

def test_basic_reversion():
    result = ParagraphPattern().revert(PARAGRAPH_BLOCK_DATA)
    assert PARAGRAPH_MD_DATA == result