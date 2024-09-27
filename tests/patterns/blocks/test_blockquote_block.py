import pytest
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern


def test_basic_conversion():
    block_data = "Blockquote content"
    block_props = {}
    
    md = [
        f"> {block_data}",
    ]
    md = "\n".join(md)
    result = BlockquotePattern().convert(md)
    
    assert isinstance(result, dict)
    assert "blockquote" == result["type"]
    assert block_props == result["props"]
    assert block_data == result["data"]



def test_basic_reversion():
    """
    """
    block = {
        "type": "blockquote",
        "props": {
        },
        "data": "Blockquote content"
    }
    
    md_data = block['data']
    md = [
        f'> {md_data}',
        f''
    ]
    md = "\n".join(md)
    
    result = BlockquotePattern().revert(block)
    assert isinstance(result, str)
    assert md == result