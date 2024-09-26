import pytest
from django_markdown_converter.patterns.blocks.footnote import FootnotePattern


def test_basic_conversion():
    block_index = "1"
    md = [
        f"[^{block_index}]:",
        "    Footnote definition.",
        "",
    ]
    md = "\n".join(md)
    output = FootnotePattern().convert(md)
    
    assert isinstance(output, dict)
    assert "footnote" == output["type"]
    assert block_index == output["props"]["index"]


def test_basic_reversion():
    """
    """
    block = {
        "type": "footnote",
        "props": {
            "index": 1,
        },
        "data": "Footnote content!"
    }
    
    md_props_index = block['props']['index']
    md_data = block['data']
    
    md = [
        f'[^{md_props_index}]:',
        f'    {md_data}',
        f''
    ]
    md = "\n".join(md)
    output = FootnotePattern().revert(block)
    assert isinstance(output, str)
    assert md == output