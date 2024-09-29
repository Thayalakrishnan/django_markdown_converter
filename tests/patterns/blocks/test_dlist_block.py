import pytest
from django_markdown_converter.patterns.blocks.dlist import DListPattern

DLIST_BLOCK_DATA = {
    "type": "dlist",
    "props": {},
    "data": {
        "term": "mole",
        "definition": ["a small burrowing mammal"],
    }
}


DLIST_MD_DATA = f'''{DLIST_BLOCK_DATA["data"]["term"]}
: {DLIST_BLOCK_DATA["data"]["definition"][0]}
'''

def test_basic_conversion():
    result = DListPattern().convert(DLIST_MD_DATA)
    assert DLIST_BLOCK_DATA == result

def test_basic_reversion():
    result = DListPattern().revert(DLIST_BLOCK_DATA)
    assert DLIST_MD_DATA == result