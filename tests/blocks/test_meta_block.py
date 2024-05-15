import pytest
from django_markdown_converter.blocks.meta import MetaBlockifier


def test_basic_conversion():
    block_type = "heading"
    block_data = "value"
    block_level = 2
    md = [
        f'---',
        f'key: {block_data}',
        f'---',
        f'',
    ]
    output = MetaBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "meta" == output["type"]
    #assert block_data == output["data"]

