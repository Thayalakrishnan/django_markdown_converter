import pytest
from django_markdown_converter.blocks.list import UnOrderedListBlockifier

def test_basic_conversion():
    md = [
        f'- UnOrdered List Item 1',
        f'- UnOrdered List Item 2',
        f'',
    ]
    output = UnOrderedListBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "list" == output["type"]
    assert "ul" == output["tag"]

