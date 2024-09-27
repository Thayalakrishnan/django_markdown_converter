import pytest
from django_markdown_converter.patterns.blocks.meta import MetaPattern

def test_basic_conversion():
    block_key_1 = "title"
    block_value_1 = "meta block test"
    block_key_2 = "author"
    block_value_2 = "lawen t"
    
    md = [
        f'---',
        f'{block_key_1}: {block_value_1}',
        f'{block_key_2}: {block_value_2}',
        f'---',
        f'',
    ]
    
    md = "\n".join(md)
    result = MetaPattern().convert(md)
    
    assert isinstance(result, dict)
    assert "meta" == result["type"]
    assert block_value_1 == result["data"][block_key_1]
    assert block_value_2 == result["data"][block_key_2]
    #assert block_data == result["data"]


def test_basic_reversion():
    """
    """
    block_key_1 = "title"
    block_value_1 = "meta block test"
    block_key_2 = "author"
    block_value_2 = "lawen t"
    
    block = {
        "type": "meta",
        "props": {},
        "data": {
            f"{block_key_1}": f"{block_value_1}",
            f"{block_key_2}": f"{block_value_2}",
        }
    }
    md = [
        f'---',
        f'{block_key_1}: {block_value_1}',
        f'{block_key_2}: {block_value_2}',
        f'---',
    ]
    md = "\n".join(md)
    result = MetaPattern().revert(block)
    assert isinstance(result, str)
    assert md == result