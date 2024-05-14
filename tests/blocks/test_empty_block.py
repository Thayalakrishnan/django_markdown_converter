import pytest
from django_markdown_converter.blocks.empty import EmptyBlockifier


def test_basic_conversion():
    md = ["",]
    output = EmptyBlockifier().blockify(md)
    assert isinstance(output, dict)

