import pytest
from django_markdown_converter.patterns.blocks.svg import SVGPattern

SVG_BLOCK_DATA = {
    "type": "svg",
    "props": {
        "title": "graphic title"
    },
    "data": "content"
}


SVG_MD_DATA = f'''<svg title="graphic title">{SVG_BLOCK_DATA["data"]}</svg>'''

def test_basic_conversion():
    result = SVGPattern().convert(SVG_MD_DATA)
    assert SVG_BLOCK_DATA == result

def test_basic_reversion():
    result = SVGPattern().revert(SVG_BLOCK_DATA)
    assert SVG_MD_DATA == result