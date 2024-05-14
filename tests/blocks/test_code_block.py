import pytest
from django_markdown_converter.blocks.code import CodeBlockifier


def test_basic_conversion():
    block_prop_language = "python"
    md = [
        f'``` {{ language="{block_prop_language}" }}',
        f'for i in range(5):',
        f'   print(i)',
        f'```',
    ]
    output = CodeBlockifier().blockify(md)
    assert isinstance(output, dict)
    assert "code" == output["type"]
    assert block_prop_language == output["props"]["language"]
    #assert heading_data == output["data"]

