import pytest
from django_markdown_converter.patterns.blocks.list import OListPattern


def test_basic_conversion():
    block_list_items = [
        "List Item 1",
        "List Item 2",
        "List Item 3",
    ]
    
    md = [
        f'1. {block_list_items[0]}',
        f'2. {block_list_items[1]}',
        f'3. {block_list_items[2]}',
        f'',
    ]
    
    md = "\n".join(md)
    output = OListPattern().convert(md)
    
    assert isinstance(output, dict)
    assert "olist" == output["type"]
    assert isinstance(output["data"], list)
    for index, item in enumerate(output["data"]):
        assert item["type"] == "item"
        assert item["data"] == [block_list_items[index]]


def test_basic_reversion():
    """
    """
    block_list_items = [
        "List Item 1",
        "List Item 2",
        "List Item 3",
    ]
        
    block = {
        "type": "olist",
        "props": {
        },
        "data": [
            {
                "type": "item",
                "data": [block_list_items[0]]
            },
            {
                "type": "item",
                "data": [block_list_items[1]]
            },
            {
                "type": "item",
                "data": [block_list_items[2]]
            },
        ]
    }
    
    md = [
        f'1. {block_list_items[0]}',
        f'2. {block_list_items[1]}',
        f'3. {block_list_items[2]}',
    ]
    
    md = "\n".join(md)
    output = OListPattern().revert(block)
    assert isinstance(output, str)
    assert md == output