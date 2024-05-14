import pytest
from django_markdown_converter.blocks.list import ListBlockifier


def test_basic_conversion():
    md = [
        f'- list item 1',
        f'- list item 2',
        f'',
    ]
    output = ListBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "list" == output["type"]
    assert "ul" == output["tag"]

