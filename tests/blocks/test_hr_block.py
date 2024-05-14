import pytest
from django_markdown_converter.blocks.hr import HRBlockifier


def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    output = HRBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "hr" == output["type"]
    #assert block_data == output["data"]

