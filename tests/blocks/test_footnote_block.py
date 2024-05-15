import pytest
from django_markdown_converter.blocks.footnote import FootnoteBlockifier


def test_basic_conversion():
    md = [
        #"Voluptatem eos aperiam dolorem numquam quisquam [^1]. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. ",
        "[^1]:",
        "    Footnote definition.",
        "",
    ]
    blockifier = FootnoteBlockifier()
    output = blockifier.blockify(md)
    output = blockifier.getFootnotes()
    print(output)
    assert isinstance(output, dict)
    assert "footnotes" == output["type"]
    #assert heading_id == output["props"]["id"]
    #assert heading_level == output["props"]["level"]
    #assert heading_data == output["data"]

