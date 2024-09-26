import pytest
from django_markdown_converter.patterns.blocks.table import TablePattern

def test_basic_conversion():
    md = [
        f'| column 1 | column 2 |',
        f'| --- | --- |',
        f'|row 1 col 1|row 1 col 2|',
        f'|row 2 col 1|row 2 col 2|',
        f'',
    ]
    md = "\n".join(md)
    output = TablePattern().convert(md)
    
    assert isinstance(output, dict)
    assert "table" == output["type"]
    
    assert "header" in output["data"]
    assert "body" in output["data"]
    
    assert isinstance(output["data"]["header"], list)
    assert isinstance(output["data"]["body"], list)
    

def test_basic_reversion():
    """
    """
    header = ["column 1", "column 2"]
    body = [
        ["row 1 col 1", "row 1 col 2"], 
        ["row 2 col 1", "row 2 col 2"]
    ]
    
    block = {
        "type": "table",
        "props": {},
        "data": {
            "header": header,
            "body": body
        }
    }
    md = [
        f'| {header[0]} | {header[1]} |',
        f'| --- | --- |',
        f'| {body[0][0]} | {body[0][1]} |',
        f'| {body[1][0]} | {body[1][1]} |',
        f'',
    ]
    
    md = "\n".join(md)
    output = TablePattern().revert(block)
    assert isinstance(output, str)
    assert md == output