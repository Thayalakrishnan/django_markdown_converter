import pytest
from django_markdown_converter.blocks.table import TableBlockifier


def test_basic_conversion():
    md = """
    | { id="small-table" caption="small table of values" } |
    | Column 1 Title | Column 2 Title |
    | ----------- | ----------- |
    | Row 1 Column 1| Row 1 Column 2 |
    | Row 2 Column 1| Row 2 Column 2 |
    """
    
    md = [
        f'| column 1 | column 2 |',
        f'| --- | --- |',
        f'|row 1 col 1|row 1 col 2|',
        f'|row 2 col 1|row 2 col 2|',
        f'{{ id="small-table" caption="small table of values" }}',
        #f'',
    ]
    output = TableBlockifier().blockify(md)
    assert isinstance(output, dict)
    print(md)
    print(output)
    assert "table" == output["type"]
    assert isinstance(output, bool)
    #assert block_data == output["data"]

