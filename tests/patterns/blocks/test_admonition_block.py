import pytest
from django_markdown_converter.patterns.blocks.admonition import AdmonitionPattern
from django_markdown_converter.patterns.data import ADMONITION_PATTERN


def test_basic_conversion():
    """
    note, admonition content is indented
    """
    block_data = "Admonition content!"
    block_prop_type = "note"
    block_prop_title = "Note Title"
    
    md = [
        f'!!! {block_prop_type} "{block_prop_title}"',
        f"    {block_data}",
        #"",
    ]
    md = "\n".join(md)
    
    output = AdmonitionPattern(ADMONITION_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "admonition" == output["type"]
    assert block_prop_type == output["props"]["type"]
    assert block_prop_title == output["props"]["title"]
    assert block_data == output["data"]
