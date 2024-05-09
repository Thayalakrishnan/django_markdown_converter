import pytest
from django_markdown_converter.blockifiers.blocks.paragraph import ParagraphBlockifier


def test_basic_usage():
    md = ["This is a paragraph after a heading. ", ""]
    output = ParagraphBlockifier().blockify(md)
    print(output)
    assert isinstance(output, dict)
