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
    output = DListPattern(DLIST_PATTERN).convert(md)
    assert isinstance(output, dict)
    assert "dlist" == output["type"]
    assert block_data_term == output["data"]["term"]
    assert block_data_definition in output["data"]["definition"]


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
    output = DListPattern().revert(block)
    assert isinstance(output, str)
    assert md == output