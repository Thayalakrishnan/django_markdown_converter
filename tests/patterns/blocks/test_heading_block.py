import pytest
from django_markdown_converter.patterns.blocks.heading import HeadingPattern



def test_heading_levels():
    # test heading level 0 - 7
    for i in range(1, 7):
        md = f"{'#'*i} This heading level {i}"
        result = HeadingPattern().convert(md)
        assert isinstance(result, dict)

def test_not_heading():
    """
    return an empty dict as no heading has been detected
    """
    md = "This is not a heading"
    result = HeadingPattern().convert(md)
    assert isinstance(result, dict)
    assert len(result.keys()) == 0


def test_heading_with_extra_content():
    """
    return an empty dict as no heading has been detected
    """
    md = ["### This is a heading", "This is a sentence after the heading."]
    md = "\n".join(md)
    result = HeadingPattern().convert(md)
    assert isinstance(result, dict)

HEADING_BLOCK_DATA = {
    "type": "heading",
    "props": {
        "level": 2,
    },
    "data": "Example Heading"
}


HEADING_MD_DATA = f'''## {HEADING_BLOCK_DATA["data"]}'''


def test_basic_conversion():
    result = HeadingPattern().convert(HEADING_MD_DATA)
    assert HEADING_BLOCK_DATA == result

def test_basic_reversion():
    result = HeadingPattern().revert(HEADING_BLOCK_DATA)
    assert HEADING_MD_DATA == result
