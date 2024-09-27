import pytest

from django_markdown_converter.convert import Convert

def test_basic_conversion():
    expected = [
        {"type": "heading", "props": {"level": 1}, "data": "Heading 1"},
        {"type": "paragraph", "props": {}, "data": "This is a paragraph after a heading."},
    ]
    
    md = [
    "# Heading 1",
    "",
    "This is a paragraph after a heading."
    "",
    ]
    md = "\n".join(md)
    
    output = Convert(md)
    
    assert isinstance(output, list)
    assert expected == output
    
    for block_e, block_o in zip(expected, output):
        assert block_e["type"] == block_o["type"]
        assert block_e["data"] == block_o["data"]



