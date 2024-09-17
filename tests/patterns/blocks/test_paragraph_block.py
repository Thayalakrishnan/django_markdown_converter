import pytest
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern
from django_markdown_converter.patterns.lookups import PARAGRAPH_PATTERN


def test_basic_conversion():
    """
    this will need to change once we move off paragraphs returning lists
    """
    md = [
        "This is the first paragraph. ", 
        #"This is the second paragraph. ", 
        ]
    output = ParagraphPattern().convert(md)[0]
    print(output)
    #assert isinstance(output, list)
    #assert isinstance(output, bool)
    assert "paragraph" == output["type"]
