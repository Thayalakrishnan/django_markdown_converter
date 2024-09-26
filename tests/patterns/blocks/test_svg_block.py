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
    output = SVGPattern().convert(md)
    assert isinstance(output, dict)
    assert "svg" == output["type"]
    assert block_data == output["data"]


def test_basic_reversion():
    block_data = "content"
    block = {
        "type": "svg",
        "props": {
        },
        "data": block_data
    }
    
    md = [
        f'<svg>',
        f'{block_data}',
        f'</svg>',
    ]
    md = "\n".join(md)
    output = SVGPattern().revert(block)
    assert isinstance(output, str)
    assert md == output