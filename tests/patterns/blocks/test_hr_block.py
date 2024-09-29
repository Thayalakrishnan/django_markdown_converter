import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern

HR_BLOCK_DATA = {
    "type": "hr",
    "props": {},
    "data": "---"
}


HR_MD_DATA = f'''---'''

def test_basic_conversion():
    result = HRPattern().convert(HR_MD_DATA)
    assert HR_BLOCK_DATA == result

def test_basic_reversion():
    result = HRPattern().revert(HR_BLOCK_DATA)
    assert HR_MD_DATA == result