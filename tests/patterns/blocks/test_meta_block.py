import pytest
from django_markdown_converter.patterns.blocks.meta import MetaPattern
from django_markdown_converter.patterns.data import META_PATTERN


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
    output = MetaPattern(META_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "meta" == output["type"]
    assert block_value_1 == output["data"][block_key_1]
    assert block_value_2 == output["data"][block_key_2]
    #assert block_data == output["data"]

