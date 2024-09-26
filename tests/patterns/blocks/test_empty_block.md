import pytest
from django_markdown_converter.patterns.blocks.empty import EmptyPattern


def test_basic_conversion():
    md = ["This is some markdown",]
    output = EmptyPattern().convert(md)
    assert isinstance(output, dict)

