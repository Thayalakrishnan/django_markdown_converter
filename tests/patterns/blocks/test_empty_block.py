import pytest
from django_markdown_converter.patterns.blocks.empty import EmptyPattern


def test_basic_conversion():
    md = ["",]
    output = EmptyPattern().blockify(md)
    assert isinstance(output, dict)

