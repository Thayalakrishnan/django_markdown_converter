import pytest
from django_markdown_converter.patterns.blocks.heading import HeadingPattern

def test_basic_conversion():
    heading_type = "heading"
    heading_data = "This is a heading"
    heading_id = heading_data.lower().replace(" ", "-")
    heading_level = 2
    heading_raw = f"{'#'*heading_level} {heading_data}"
    md = heading_raw
    
    output = HeadingPattern().convert(md)
    assert isinstance(output, dict)
    assert heading_type == output["type"]
    #assert heading_id == output["props"]["id"]
    assert heading_level == output["props"]["level"]
    assert heading_data == output["data"]

def test_heading_levels():
    # test heading level 0 - 7
    for i in range(1, 7):
        md = f"{'#'*i} This heading level {i}"
        output = HeadingPattern().convert(md)
        assert isinstance(output, dict)

def test_not_heading():
    """
    return an empty dict as no heading has been detected
    """
    md = "This is not a heading"
    output = HeadingPattern().convert(md)
    assert isinstance(output, dict)
    assert len(output.keys()) == 0


def test_heading_with_extra_content():
    """
    return an empty dict as no heading has been detected
    """
    md = ["### This is a heading", "This is a sentence after the heading."]
    md = "\n".join(md)
    output = HeadingPattern().convert(md)
    assert isinstance(output, dict)
    
    
    

def test_basic_reversion():
    """
    """
    block = {
        "type": "heading",
        "props": {
            "level": 2,
            "id": "Example Note",
        },
        "data": "Heading content!"
    }
    
    md_props_level = block['props']['level']
    md_data = block['data']
    
    md = [
        '#'*md_props_level + f' {md_data}',
        f''
    ]
    md = "\n".join(md)
    output = HeadingPattern().revert(block)
    assert isinstance(output, str)
    assert md == output