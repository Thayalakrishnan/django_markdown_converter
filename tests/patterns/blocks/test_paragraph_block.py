import pytest
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern
from django_markdown_converter.patterns.lookups import PARAGRAPH_PATTERN


def test_basic_conversion():
    """
    this will need to change once we move off paragraphs returning lists
    """
    block_data_sentence_1 = "This is the first sentence in the paragraph. "
    
    md = [
        f"{block_data_sentence_1}", 
        ""
    ]
    md = "\n".join(md)
    output = ParagraphPattern(PARAGRAPH_PATTERN).convert(md)
    
    assert "paragraph" == output["type"]
    assert isinstance(output["data"], str)
    assert block_data_sentence_1 == output["data"]
