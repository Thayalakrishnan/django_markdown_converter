import pytest
from django_markdown_converter.patterns.blocks.image import ImagePattern
from django_markdown_converter.patterns.lookups import IMAGE_PATTERN


def test_basic_conversion():
    block_prop_alt = "Image alt text"
    block_prop_title = "Image title"
    block_prop_src = "https://www.testimage.com/1920/1080"
    
    md = [
        f'![ {block_prop_alt} ]({block_prop_src} "{block_prop_title}")',
        f'',
    ]
    md = "\n".join(md)
    output = ImagePattern(IMAGE_PATTERN).convert(md)
    
    assert isinstance(output, dict)
    assert "image" == output["type"]
    assert block_prop_title == output["props"]["title"]
    assert block_prop_alt == output["props"]["alt"]
    assert block_prop_src == output["data"]

