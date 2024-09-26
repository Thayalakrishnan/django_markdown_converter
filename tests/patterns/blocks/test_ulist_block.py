import pytest
from django_markdown_converter.patterns.blocks.list import UListPattern

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
    output = UListPattern().convert(md)
    
    assert isinstance(output, dict)
    assert "ulist" == output["type"]
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
        "type": "ulist",
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
        f'- {block_list_items[0]}',
        f'- {block_list_items[1]}',
        f'- {block_list_items[2]}',
    ]

    md = "\n".join(md)
    output = UListPattern().revert(block)
    assert isinstance(output, str)
    assert md == output