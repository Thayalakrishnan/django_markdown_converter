import pytest
from django_markdown_converter.blocks.admonition import AdmonitionBlockifier


def test_basic_conversion():
    block_data = "Admonition content"
    block_prop_type = "note"
    block_prop_title = "Note Title"
    
    md = [
        f"!!! {block_prop_type} {block_prop_title}",
        f"{block_data}",
        #"More admonition content",
        "",
    ]
    
    output = AdmonitionBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "admonition" == output["type"]
    assert block_prop_type == output["props"]["type"]
    assert block_prop_title == output["props"]["title"]
    assert block_data == output["data"]
