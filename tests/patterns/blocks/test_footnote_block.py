import pytest
from django_markdown_converter.patterns.blocks.footnote import FootnotePattern
from django_markdown_converter.patterns.lookups import FOOTNOTE_PATTERN


def test_basic_conversion():
    block_index = "1"
    md = [
        f"[^{block_index}]:",
        "    Footnote definition.",
        "",
    ]
    md = "\n".join(md)
    output = FootnotePattern(FOOTNOTE_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "footnote" == output["type"]
    assert block_index == output["props"]["index"]

