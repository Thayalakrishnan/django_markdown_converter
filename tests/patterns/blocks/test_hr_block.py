import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern


def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    output = HRPattern().blockify(md)
    assert isinstance(output, dict)
    assert "hr" == output["type"]
    #assert block_data == output["data"]

