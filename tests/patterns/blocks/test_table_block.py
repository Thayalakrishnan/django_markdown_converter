import pytest
from django_markdown_converter.patterns.blocks.table import TablePattern
from django_markdown_converter.patterns.data import TABLE_PATTERN


def test_basic_conversion():
    md = [
        f'| column 1 | column 2 |',
        f'| --- | --- |',
        f'|row 1 col 1|row 1 col 2|',
        f'|row 2 col 1|row 2 col 2|',
        f'',
    ]
    md = "\n".join(md)
    output = TablePattern(TABLE_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "table" == output["type"]
    
    assert "header" in output["data"]
    assert "body" in output["data"]
    
    assert isinstance(output["data"]["header"], list)
    assert isinstance(output["data"]["body"], list)
    
