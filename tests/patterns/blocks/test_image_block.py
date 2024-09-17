import pytest
from django_markdown_converter.patterns.blocks.image import ImagePattern
from django_markdown_converter.patterns.lookups import IMAGE_PATTERN


def test_basic_conversion():
    block_prop_title = "Image Title"
    block_prop_src = "https://www.testimage.com/1920/1080"
    
    md = [
        f'![ title="{block_prop_title}" ]({block_prop_src})',
        f'',
    ]
    output = ImagePattern().convert(md)
    assert isinstance(output, dict)
    assert "image" == output["type"]
    assert block_prop_title == output["props"]["title"]
    assert block_prop_src == output["data"]

