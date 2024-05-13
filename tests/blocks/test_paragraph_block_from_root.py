import pytest
from django_markdown_converter.blocks.paragraph import ParagraphBlockifier


def test_basic_usage():
    md = [
        "This is the first paragraph. ", 
        "",
        "This is the second paragraph. ", 
        ]
    output = ParagraphBlockifier().blockify(md)
    print(output)
    #assert isinstance(output, list)
    assert isinstance(output, bool)
