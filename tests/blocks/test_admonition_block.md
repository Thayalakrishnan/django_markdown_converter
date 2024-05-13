import pytest
from django_markdown_converter.blocks.admonition import AdmonitionBlockifier


def test_basic_conversion():
    block_data = "This is a heading"
    block_level = 2
    
    block_raw = f"{'#'*heading_level} {heading_data}"
    md = [heading_raw]
    
    output = AdmonitionBlockifier().blockify(md)
    
    assert isinstance(output, dict)
    assert "admonition" == output["type"]
    assert heading_id == output["props"]["id"]
    assert heading_level == output["props"]["level"]
    assert heading_data == output["data"]

def test_heading_levels():
    # test heading level 0 - 7
    for i in range(0, 8):
        md = [f"{'#'*i} This is a heading level {i}"]
        output = AdmonitionBlockifier().blockify(md)
        assert isinstance(output, dict)

def test_not_heading():
    """
    return an empty dict as no heading has been detected
    """
    md = ["This is not a heading"]
    output = AdmonitionBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert output == {}

def test_not_heading_to_many_hashes():
    """
    return an empty dict as no heading has been detected
    """
    md = ["####### This is not a heading"]
    output = AdmonitionBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert output == {}

def test_heading_with_extra_content():
    """
    return an empty dict as no heading has been detected
    """
    md = ["### This is a heading", "This is a sentence after the heading."]
    output = AdmonitionBlockifier().blockify(md)
    assert isinstance(output, dict)