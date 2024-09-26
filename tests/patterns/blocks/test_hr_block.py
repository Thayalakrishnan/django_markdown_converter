import pytest
from django_markdown_converter.patterns.blocks.hr import HRPattern

def test_basic_conversion():
    block_data = ""
    md = [
        f'***',
        f'',
    ]
    md = "\n".join(md)
    output = HRPattern().convert(md)
    assert isinstance(output, dict)
    assert "hr" == output["type"]


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
    output = HRPattern().revert(block)
    assert isinstance(output, str)
    assert md == output