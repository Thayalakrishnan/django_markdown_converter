import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern

def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    md = "\n".join(md)
    result = HRPattern().convert(md)
    assert isinstance(result, dict)
    assert "hr" == result["type"]


def test_basic_reversion():
    """
    """
    block = {
        "type": "hr",
        "props": {
        },
        "data": "---"
    }
    md_data = block['data']
    md = [
        f'{md_data}',
        f''
    ]
    md = "\n".join(md)
    result = HRPattern().revert(block)
    assert isinstance(result, str)
    assert md == result