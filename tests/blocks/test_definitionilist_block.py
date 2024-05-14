import pytest
from django_markdown_converter.blocks.definitionlist import DefinitionListBlockifier


def test_basic_conversion():
    block_data_term = f"yeet"
    block_data_definition = f"to throw!"
    
    md = [
        f": {block_data_term}",
        f": {block_data_definition}",
        "",
    ]
    output = DefinitionListBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "definitions" == output["type"]
    assert block_data_term == output["data"]["term"]
    assert block_data_definition == output["data"]["definition"]

