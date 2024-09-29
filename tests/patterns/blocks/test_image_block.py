import pytest
from django_markdown_converter.patterns.blocks.image import ImagePattern

    
IMAGE_BLOCK_DATA = {
    "type": "image",
    "props": {
        "alt": "Alt text for image",
        "title": "Title for image"
    },
    "data": "https://src-image.com/image.jpg"
}


IMAGE_MD_DATA = f'''![{IMAGE_BLOCK_DATA["props"]["alt"]}]({IMAGE_BLOCK_DATA["data"]} \"{IMAGE_BLOCK_DATA["props"]["title"]}\")'''

def test_basic_conversion():
    result = ImagePattern().convert(IMAGE_MD_DATA)
    assert IMAGE_BLOCK_DATA == result

def test_basic_reversion():
    result = ImagePattern().revert(IMAGE_BLOCK_DATA)
    assert IMAGE_MD_DATA == result