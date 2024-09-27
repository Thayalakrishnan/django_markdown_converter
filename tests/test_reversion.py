import pytest

from django_markdown_converter.revert import Revert

def test_basic_reversion():
    blocks = [
        {"type": "heading", "props": {"level": 1}, "data": "Heading 1"},
        {"type": "paragraph", "props": {}, "data": "This is a paragraph after a heading."},
    ]
    
    expected = [
    "# Heading 1",
    "",
    "This is a paragraph after a heading.",
    "",
    ]
    expected = "\n".join(expected)
    result = Revert(blocks)
    assert isinstance(result, str)
    assert expected == result
