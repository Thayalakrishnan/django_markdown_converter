import pytest
from django_markdown_converter.helpers.processors import remove_trailing_whitespace


def test_basic_conversion():
    """
    poetry run python -m pytest .\tests\helpers\test_processors.py
    
    """
    content = [
    "this is some content with trailing whitespace.   ",
    "this is some content with trailing whitespace.   ",
    "this is some content with trailing whitespace.   ",
    ]
    expected = [
    "this is some content with trailing whitespace.",
    "this is some content with trailing whitespace.",
    "this is some content with trailing whitespace.",
    ]
    
    content = "\n".join(content)
    expected = "\n".join(expected)
    
    ret = remove_trailing_whitespace(content)
    
    assert isinstance(ret, str)
    assert expected == ret
