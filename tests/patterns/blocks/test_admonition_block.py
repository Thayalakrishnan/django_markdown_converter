import pytest
from django_markdown_converter.patterns.blocks.admonition import AdmonitionPattern

ADMONITION_BLOCK_DATA = {
    "type": "admonition",
    "props": {
        "type": "note",
        "title": "Note Title",
    },
    "data": "Admonition content!"
}

ADMONITION_MD_DATA = f'''!!! {ADMONITION_BLOCK_DATA["props"]["type"]} \"{ADMONITION_BLOCK_DATA["props"]["title"]}\"
    {ADMONITION_BLOCK_DATA["data"]}'''

def test_basic_conversion():
    """
    note, admonition content is indented
    """
    result = AdmonitionPattern().convert(ADMONITION_MD_DATA)
    assert ADMONITION_BLOCK_DATA == result


def test_basic_reversion():
    """
    note, admonition content is indented
    """
    result = AdmonitionPattern().revert(ADMONITION_BLOCK_DATA)
    assert ADMONITION_MD_DATA == result