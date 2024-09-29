import pytest
from django_markdown_converter.patterns.blocks.table import TablePattern

TABLE_BLOCK_DATA = {
    "type": "table",
    "props": {},
    "data": {
        "header": ["column 1", "column 2"],
        "body": [
            ["row 1 col 1", "row 1 col 2"], 
            ["row 2 col 1", "row 2 col 2"]         
        ]
    }
}


TABLE_MD_DATA = f'''| {TABLE_BLOCK_DATA["data"]["header"][0]} | {TABLE_BLOCK_DATA["data"]["header"][1]} |
| --- | --- |
| {TABLE_BLOCK_DATA["data"]["body"][0][0]} | {TABLE_BLOCK_DATA["data"]["body"][0][1]} |
| {TABLE_BLOCK_DATA["data"]["body"][1][0]} | {TABLE_BLOCK_DATA["data"]["body"][1][1]} |
'''

def test_basic_conversion():
    result = TablePattern().convert(TABLE_MD_DATA)
    assert  TABLE_BLOCK_DATA == result

def test_basic_reversion():
    result = TablePattern().revert(TABLE_BLOCK_DATA)
    assert  TABLE_MD_DATA == result