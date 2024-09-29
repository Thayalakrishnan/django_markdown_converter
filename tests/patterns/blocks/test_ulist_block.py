import pytest
from django_markdown_converter.patterns.blocks.list import UListPattern
    
ULIST_BLOCK_DATA = {
    "type": "ulist",
    "props": {},
    "data": [
        {
            "type": "item",
            "data": ["List Item 1"]
        },
        {
            "type": "item",
            "data": ["List Item 2"]
        },
        {
            "type": "item",
            "data": ["List Item 3"]
        },
    ]
}


ULIST_MD_DATA = f'''- {ULIST_BLOCK_DATA["data"][0]["data"][0]}
- {ULIST_BLOCK_DATA["data"][1]["data"][0]}
- {ULIST_BLOCK_DATA["data"][2]["data"][0]}'''

def test_basic_conversion():
    result = UListPattern().convert(ULIST_MD_DATA)
    assert ULIST_BLOCK_DATA == result

def test_basic_reversion():
    result = UListPattern().revert(ULIST_BLOCK_DATA)
    assert ULIST_MD_DATA == result