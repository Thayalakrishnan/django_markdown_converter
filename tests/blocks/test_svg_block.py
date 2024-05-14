import pytest
from django_markdown_converter.blocks.svg import SVGBlockifier


def test_basic_conversion():
    block_data = "content"
    md = [
        r'<svg title="graphic title" >',
        f'{block_data}',
        r'</svg>',
    ]
    output = SVGBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "svg" == output["type"]
#    assert block_data == output["data"]

