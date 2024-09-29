import pytest
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern

BLOCKQUOTE_BLOCK_DATA = {
    "type": "blockquote",
    "props": {},
    "data": "Blockquote content"
}

BLOCKQUOTE_MD_DATA = f'''> {BLOCKQUOTE_BLOCK_DATA["data"]}'''


def test_basic_conversion():
    result = BlockquotePattern().convert(BLOCKQUOTE_MD_DATA)
    assert BLOCKQUOTE_BLOCK_DATA == result


def test_basic_reversion():
    result = BlockquotePattern().revert(BLOCKQUOTE_BLOCK_DATA)
    assert BLOCKQUOTE_MD_DATA == result