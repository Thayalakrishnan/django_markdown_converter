import pytest
from django_markdown_converter.patterns.blocks.code import CodePattern

CODE_BLOCK_DATA = {
    "type": "code",
    "props": {
        "language": "python"
    },
    "data": [
        [("k", "for"), ("w", " "), ("n", "i"), ("w", " "), ("ow", "in"), ("w", " "), ("nb", "range"), ("p", "("), ("mi", "5"), ("p", ")"), ("p",":")],
        [("w", "    "), ("nb", "print"), ("p", "("), ("n", "i"), ("p", ")")]
    ]
}

CODE_MD_DATA  = """```python
for i in range(5):
    print(i)
```
"""


def test_basic_conversion():
    result = CodePattern().convert(CODE_MD_DATA)
    assert CODE_BLOCK_DATA == result


def test_basic_reversion():
    result = CodePattern().revert(CODE_BLOCK_DATA)
    assert CODE_MD_DATA == result
    
