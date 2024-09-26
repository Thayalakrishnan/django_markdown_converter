import pytest
from django_markdown_converter.patterns.blocks.blockquote import BlockquotePattern


def test_basic_conversion():
    block_data = "Blockquote content"
    block_props = {}
    
    md = [
        f"> {block_data}",
    ]
    md = "\n".join(md)
    output = BlockquotePattern().convert(md)
    
    assert isinstance(output, dict)
    assert "blockquote" == output["type"]
    assert block_props == output["props"]
    assert block_data == output["data"]



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
    
    output = BlockquotePattern().revert(block)
    assert isinstance(output, str)
    assert md == output