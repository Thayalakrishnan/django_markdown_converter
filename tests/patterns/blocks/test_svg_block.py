import pytest
from django_markdown_converter.patterns.blocks.svg import SVGPattern


def test_basic_conversion():
    block_data = "content"
    md = [
        r'<svg title="graphic title" >',
        f'{block_data}',
        r'</svg>',
    ]
    output = SVGPattern().blockify(md)
    assert isinstance(output, dict)
    assert "svg" == output["type"]
#    assert block_data == output["data"]

