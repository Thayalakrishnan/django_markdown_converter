import pytest
from django_markdown_converter.patterns.blocks.dlist import DListPattern
from django_markdown_converter.patterns.lookups import DLIST_PATTERN


def test_basic_conversion():
    block_data_term = f"yeet"
    block_data_definition = f"to throw!"
    
    md = [
        f"{block_data_term}",
        f": {block_data_definition}",
        "",
    ]
    md = "\n".join(md)
    output = DListPattern(DLIST_PATTERN).convert(md)
    assert isinstance(output, dict)
    assert "dlist" == output["type"]
    assert block_data_term == output["data"]["term"]
    assert block_data_definition in output["data"]["definition"]

