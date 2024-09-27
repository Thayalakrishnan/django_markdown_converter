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
    result = FootnotePattern().convert(md)
    
    assert isinstance(result, dict)
    assert "footnote" == result["type"]
    assert block_index == result["props"]["index"]


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
    result = FootnotePattern().revert(block)
    assert isinstance(result, str)
    assert md == result