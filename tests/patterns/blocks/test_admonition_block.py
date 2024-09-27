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
    
    result = AdmonitionPattern().convert(md)
    
    assert isinstance(result, dict)
    assert "admonition" == result["type"]
    assert block_prop_type == result["props"]["type"]
    assert block_prop_title == result["props"]["title"]
    assert block_data == result["data"]



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
    result = AdmonitionPattern().revert(block)
    
    print(repr(md))
    print(repr(result))
    
    assert isinstance(result, str)
    assert md == result