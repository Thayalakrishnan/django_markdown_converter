import pytest
from django_markdown_converter.patterns.blocks.table import TablePattern
from django_markdown_converter.patterns.lookups import TABLE_PATTERN


def test_basic_conversion():
    md = [
        f'| column 1 | column 2 |',
        f'| --- | --- |',
        f'|row 1 col 1|row 1 col 2|',
        f'|row 2 col 1|row 2 col 2|',
        f'{{ id="small-table" caption="small table of values" }}',
        #f'',
    ]
    output = TablePattern().convert(md)
    assert isinstance(output, dict)
    assert "table" == output["type"]
    assert "props" in output
    assert "id" in output["props"]
    assert "caption" in output["props"]
    assert "header" in output["data"]
    assert "body" in output["data"]
    #assert isinstance(output, bool)
    #assert block_data == output["data"]

