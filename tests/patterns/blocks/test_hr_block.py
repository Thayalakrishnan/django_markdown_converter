import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern
from django_markdown_converter.patterns.lookups import HR_PATTERN


def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    output = HRPattern().convert(md)
    assert isinstance(output, dict)
    assert "hr" == output["type"]
    #assert block_data == output["data"]

