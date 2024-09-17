import pytest
from django_markdown_converter.patterns.blocks.code import CodePattern
from django_markdown_converter.patterns.lookups import CODE_PATTERN


def test_basic_conversion():
    block_prop_language = "python"
    block_prop_title = "python for loop"
    block_prop_caption = "caption for the python for loop"
    
    block_props_string = f'{{ language="{block_prop_language}" title="{block_prop_title}" caption="{block_prop_caption}" }}'
    block_props = {
        "language": block_prop_language,
        "title": block_prop_title,
        "caption": block_prop_caption,
    }
    
    md = [
        f'```{block_prop_language}',
        f'for i in range(5):',
        f'   print(i)',
        f'```',
    ]
    md = "\n".join(md)
    output = CodePattern(CODE_PATTERN).convert(md, block_props_string)
    
    assert isinstance(output, dict)
    assert "code" == output["type"]
    
    assert block_prop_language == output["props"]["language"]
    assert block_prop_title == output["props"]["title"]
    assert block_prop_caption == output["props"]["caption"]

