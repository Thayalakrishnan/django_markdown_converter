import pytest
from django_markdown_converter.patterns.blocks.list import OListPattern

OLIST_BLOCK_DATA = {
    "type": "olist",
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


OLIST_MD_DATA = f'''1. {OLIST_BLOCK_DATA["data"][0]["data"][0]}
2. {OLIST_BLOCK_DATA["data"][1]["data"][0]}
3. {OLIST_BLOCK_DATA["data"][2]["data"][0]}'''

def test_basic_conversion():
    result = OListPattern().convert(OLIST_MD_DATA)
    assert OLIST_BLOCK_DATA == result

def test_basic_reversion():
    result = OListPattern().revert(OLIST_BLOCK_DATA)
    assert OLIST_MD_DATA == result