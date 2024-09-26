import pytest
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern


def test_basic_conversion():
    """
    this will need to change once we move off paragraphs returning lists
    """
    block_data_sentence_1 = "This is the first sentence in the paragraph."
    
    md = [
        f"{block_data_sentence_1}", 
        ""
    ]
    md = "\n".join(md)
    output = ParagraphPattern().convert(md)
    
    assert "paragraph" == output["type"]
    assert isinstance(output["data"], str)
    assert block_data_sentence_1 == output["data"]


def test_basic_reversion():
    """
    """
    block_data_sentence_1 = "This is the first sentence in the paragraph."
    block = {
        "type": "paragraph",
        "props": {
        },
        "data": block_data_sentence_1
    }
    
    md = [
        f'{block_data_sentence_1}',
        f''
    ]
    md = "\n".join(md)
    output = ParagraphPattern().revert(block)
    assert isinstance(output, str)
    assert md == output