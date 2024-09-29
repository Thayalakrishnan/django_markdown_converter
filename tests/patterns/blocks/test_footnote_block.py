import pytest
from django_markdown_converter.patterns.blocks.footnote import FootnotePattern

FOOTNOTE_BLOCK_DATA = {
    "type": "footnote",
    "props": {
        "index": "1",
    },
    "data": "Footnote content!"
}

FOOTNOTE_MD_DATA = f'''[^{FOOTNOTE_BLOCK_DATA["props"]["index"]}]:
    {FOOTNOTE_BLOCK_DATA["data"]}'''

def test_basic_conversion():
    result = FootnotePattern().convert(FOOTNOTE_MD_DATA)
    assert FOOTNOTE_BLOCK_DATA == result


def test_basic_reversion():
    result = FootnotePattern().revert(FOOTNOTE_BLOCK_DATA)
    assert FOOTNOTE_MD_DATA == result