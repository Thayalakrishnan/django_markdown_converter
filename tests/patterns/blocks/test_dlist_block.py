import pytest
from django_markdown_converter.patterns.blocks.dlist import DListPattern
from django_markdown_converter.patterns.data import DLIST_PATTERN


def test_basic_conversion():
    block_data_term = f"yeet"
    block_data_definition = f"to throw!"
    
    md = [
        f"{block_data_term}",
        f": {block_data_definition}",
        "",
    ]
    md = "\n".join(md)
    result = DListPattern(DLIST_PATTERN).convert(md)
    assert isinstance(result, dict)
    assert "dlist" == result["type"]
    assert block_data_term == result["data"]["term"]
    assert block_data_definition in result["data"]["definition"]


def test_basic_reversion():
    """
    """
    block = {
        "type": "dlist",
        "props": {},
        "data": {
            "term": "mole",
            "definition": ["a small burrowing mammal"],
        }
    }
    
    md_data_term = block['data']['term']
    md_data_definition = block['data']['definition'][0]
    
    md = [
        f'{md_data_term}',
        f': {md_data_definition}',
        f''
    ]
    md = "\n".join(md)
    result = DListPattern().revert(block)
    assert isinstance(result, str)
    assert md == result