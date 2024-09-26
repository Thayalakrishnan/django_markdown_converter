import pytest
from django_markdown_converter.patterns.blocks.admonition import AdmonitionPattern


def test_basic_conversion():
    """
    note, admonition content is indented
    """
    block_data = "Admonition content!"
    block_prop_type = "note"
    block_prop_title = "Note Title"
    
    md = [
        f'!!! {block_prop_type} \"{block_prop_title}\"',
        f"    {block_data}",
    ]
    md = "\n".join(md)
    
    output = AdmonitionPattern().convert(md)
    
    assert isinstance(output, dict)
    assert "admonition" == output["type"]
    assert block_prop_type == output["props"]["type"]
    assert block_prop_title == output["props"]["title"]
    assert block_data == output["data"]



def test_basic_reversion():
    """
    note, admonition content is indented
    """
    block = {
        "type": "admonition",
        "props": {
            "type": "note",
            "title": "Example Note",
        },
        "data": "Admonition content!"
    }
    
    md_props = block['props']
    md_props_type = md_props['type']
    md_props_title = md_props['title']
    md_data = block['data']
    
    md = [
        f'!!! {md_props_type} \"{md_props_title}\"',
        f'    {md_data}',
        f''
    ]
    md = "\n".join(md)
    output = AdmonitionPattern().revert(block)
    
    print(repr(md))
    print(repr(output))
    
    assert isinstance(output, str)
    assert md == output