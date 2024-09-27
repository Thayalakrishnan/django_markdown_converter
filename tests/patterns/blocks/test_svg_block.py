import pytest
from django_markdown_converter.patterns.blocks.svg import SVGPattern


def test_basic_conversion():
    block_data = "content"
    md = [
        r'<svg title="graphic title">',
        f'{block_data}',
        r'</svg>',
    ]
    md = "\n".join(md)
    result = SVGPattern().convert(md)
    assert isinstance(result, dict)
    assert "svg" == result["type"]
    assert block_data == result["data"]


def test_basic_reversion():
    block_data = "content"
    block = {
        "type": "svg",
        "props": {
        },
        "data": block_data
    }
    
    md = [
        f'<svg>{block_data}</svg>',
        f'',
    ]
    md = "\n".join(md)
    result = SVGPattern().revert(block)
    assert isinstance(result, str)
    assert md == result