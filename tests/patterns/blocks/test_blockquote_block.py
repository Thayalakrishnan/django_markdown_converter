import pytest
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern
from django_markdown_converter.patterns.data import BLOCKQUOTE_PATTERN


def test_basic_conversion():
    block_data = "Blockquote content"
    block_props = {}
    
    md = [
        f"> {block_data}",
    ]
    md = "\n".join(md)
    output = BlockquotePattern(BLOCKQUOTE_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "blockquote" == output["type"]
    assert block_props == output["props"]
    assert block_data == output["data"]
