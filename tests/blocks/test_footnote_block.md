import pytest
from django_markdown_converter.blocks.heading import HeadingBlockifier


def test_basic_conversion():
    heading_type = "heading"
    heading_data = "This is a heading"
    heading_id = heading_data.lower().replace(" ", "-")
    heading_level = 2
    heading_raw = f"{'#'*heading_level} {heading_data}"
    md = [
        "!!! note Note Title",
    ]
    output = HeadingBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert heading_type == output["type"]
    assert heading_id == output["props"]["id"]
    assert heading_level == output["props"]["level"]
    assert heading_data == output["data"]

