import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern
from django_markdown_converter.patterns.lookups import HR_PATTERN


def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    md = "\n".join(md)
    output = HRPattern(HR_PATTERN).convert(md)
    assert isinstance(output, dict)
    assert "hr" == output["type"]

