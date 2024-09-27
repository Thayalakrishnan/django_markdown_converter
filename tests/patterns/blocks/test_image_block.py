import pytest
from django_markdown_converter.patterns.blocks.image import ImagePattern


def test_basic_conversion():
    block_prop_alt = "Image alt text"
    block_prop_title = "Image title"
    block_prop_src = "https://www.testimage.com/1920/1080"
    
    md = [
        f'![ {block_prop_alt} ]({block_prop_src} "{block_prop_title}")',
        f'',
    ]
    md = "\n".join(md)
    result = ImagePattern().convert(md)
    
    assert isinstance(result, dict)
    assert "image" == result["type"]
    assert block_prop_title == result["props"]["title"]
    assert block_prop_alt == result["props"]["alt"]
    assert block_prop_src == result["data"]


def test_basic_reversion():
    """
    ![Alt text for image](https://srcimage.com/image.jpg "Title for image")
    """
    md_alt = "Alt text for image"
    md_title = "Title for image"
    md_data = "https://srcimage.com/image.jpg"
    
    block =     {
        "type": "image",
        "props": {
            "alt": md_alt,
            "title": md_title
        },
        "data": md_data
    }
    
    md = [
        f'![{md_alt}]({md_data} \"{md_title}\")',
        f''
    ]
    md = "\n".join(md)
    result = ImagePattern().revert(block)
    assert isinstance(result, str)
    assert md == result