import pytest
from django_markdown_converter.blocks.table import TableBlockifier


def test_basic_conversion():
    md = [
        f'| column 1 | column 2 |',
        f'| --- | --- |',
        f'| row 1 col 1 | row 1 col 2 |',
        f'| row 2 col 1 | row 2 col 2 |',
        f'\n',
    ]
    output = TableBlockifier().blockify(md)
    assert isinstance(output, dict)
    print(md)
    print(output)
    assert "table" == output["type"]
    #assert block_data == output["data"]

