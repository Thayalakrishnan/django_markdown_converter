import pytest
from django_markdown_converter.patterns.blocks.list import ListPattern
from django_markdown_converter.patterns.lookups import LIST_PATTERN


"""
{
    "type": "ulist",
    "props": {},
    "data": [
        {
            "type": "item",
            "data": "Item 1"
        },
        {
            "type": "item",
            "data": "Item 2"
        },
        {
            "type": "item",
            "data": "Item 3"
        },
        {
            "type": "item",
            "data": "Item 4"
        }
    ]
}
"""

def test_basic_conversion():
    block_list_items = [
        "List Item 1",
        "List Item 2",
        "List Item 3",
    ]
    
    md = [
        f'- {block_list_items[0]}',
        f'- {block_list_items[1]}',
        f'- {block_list_items[2]}',
        f'',
    ]
    
    md = "\n".join(md)
    output = ListPattern(LIST_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "olist" == output["type"]
    assert isinstance(output["data"], list)
    for index, item in enumerate(output["data"]):
        assert item["type"] == "item"
        assert item["data"] == block_list_items[index]

