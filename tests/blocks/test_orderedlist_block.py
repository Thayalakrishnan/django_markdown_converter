import pytest
from django_markdown_converter.blocks.list import OrderedListBlockifier


def test_basic_conversion():
    md = [
        f'1. Ordered List Item 1',
        f'2. Ordered List Item 2',
        f'',
    ]
    output = OrderedListBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "list" == output["type"]
    assert "ol" == output["tag"]

