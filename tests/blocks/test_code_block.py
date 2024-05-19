import pytest
from django_markdown_converter.blocks.code import CodeBlockifier


def test_basic_conversion():
    block_prop_language = "python"
    block_prop_title = "python for loop"
    block_prop_caption = "caption for the python for loop"
    md = [
        f'``` {{ language="{block_prop_language}" title="{block_prop_title}" caption="{block_prop_caption}" }}',
        f'for i in range(5):',
        f'   print(i)',
        f'```',
    ]
    output = CodeBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "code" == output["type"]
    assert block_prop_language == output["props"]["language"]
    assert block_prop_title == output["props"]["title"]
    assert block_prop_caption == output["props"]["caption"]
    #assert heading_data == output["data"]

