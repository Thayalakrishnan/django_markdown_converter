import pytest
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern
from django_markdown_converter.patterns.lookups import BLOCKQUOTE_PATTERN


def test_basic_conversion():
    block_data = "Blockquote content"
    block_prop_key = "value"
    
    md = [
        f"> {block_data}",
        f"> {block_data}",
    ]
    md = "\n".join(md)
    output = BlockquotePattern(BLOCKQUOTE_PATTERN).blockify(md)
    
    assert isinstance(output, dict)
    assert "blockquote" == output["type"]
    assert block_prop_key == output["props"]["key"]
    assert block_data == output["data"]
