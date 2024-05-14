import pytest
from django_markdown_converter.blocks.blockquote import BlockquoteBlockifier


def test_basic_conversion():
    block_data = "Blockquote content"
    block_prop_key = "value"
    
    md = [
        f'> {{ key="{block_prop_key}" }}',
        f"> {block_data}",
        "",
    ]
    
    output = BlockquoteBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "blockquote" == output["type"]
    assert block_prop_key == output["props"]["key"]
    assert block_data == output["data"]
