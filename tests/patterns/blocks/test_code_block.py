import pytest
from django_markdown_converter.patterns.blocks.code import CodePattern

    
"""
    ```python
for i in range(5):
    print(i)
```
"""

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
    result = CodePattern().convert(md, block_props_string)
    
    assert isinstance(result, dict)
    assert "code" == result["type"]
    
    assert block_prop_language == result["props"]["language"]
    assert block_prop_title == result["props"]["title"]
    assert block_prop_caption == result["props"]["caption"]



def test_basic_reversion():
    """
    """
    block = {
        "type": "code",
        "props": {
            "language": "python"
        },
        "data": [
            [["k", "for"], ["w", " "], ["n", "i"], ["w", " "], ["ow", "in"], ["w", " "], ["nb", "range"], ["p", "("], ["mi", "5"], ["p", ")"], ["p",":"]],
            [["w", "    "], ["nb", "print"], ["p", "("], ["n", "i"], ["p", ")"]]
        ]
    }
    
    md_props_language = block['props']['language']
    md_data = block['data']
    
    md = [
        f'```{md_props_language}',
        f'for i in range(5):',
        f'    print(i)',
        f'```',
        f'',
    ]
    md = "\n".join(md)
    result = CodePattern().revert(block)
    assert isinstance(result, str)
    assert md == result
    
