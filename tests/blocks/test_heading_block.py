import pytest
from django_markdown_converter.blocks.heading import HeadingBlockifier


def test_basic_conversion():
    heading_type = "heading"
    heading_data = "This is a heading"
    heading_id = heading_data.lower().replace(" ", "-")
    heading_level = 2
    heading_raw = f"{'#'*heading_level} {heading_data}"
    md = [heading_raw]
    output = HeadingBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert heading_type == output["type"]
    assert heading_id == output["props"]["id"]
    assert heading_level == output["props"]["level"]
    assert heading_data == output["data"]

def test_heading_levels():
    # test heading level 0 - 7
    for i in range(0, 8):
        md = [f"{'#'*i} This is a heading level {i}"]
        output = HeadingBlockifier().blockify(md)
        assert isinstance(output, dict)

def test_not_heading():
    """
    return an empty dict as no heading has been detected
    """
    md = ["This is not a heading"]
    output = HeadingBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert output == {}

def test_not_heading_to_many_hashes():
    """
    return an empty dict as no heading has been detected
    """
    md = ["####### This is not a heading"]
    output = HeadingBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert output == {}

def test_heading_with_extra_content():
    """
    return an empty dict as no heading has been detected
    """
    md = ["### This is a heading", "This is a sentence after the heading."]
    output = HeadingBlockifier().blockify(md)
    assert isinstance(output, dict)