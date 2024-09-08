import pytest
from django_markdown_converter.helpers.processors import remove_trailing_whitespace, process_meta_block

"""
poetry run python -m pytest tests.helpers.test_processors.py
"""

def test_basic_conversion():
    """
    """
    content = [
    "this is some content with trailing whitespace.   ",
    "this is some content with trailing whitespace.   ",
    "this is some content with trailing whitespace.   ",
    ]
    expected = [
    "this is some content with trailing whitespace.",
    "this is some content with trailing whitespace.",
    "this is some content with trailing whitespace.",
    ]
    
    content = "\n".join(content)
    expected = "\n".join(expected)
    
    ret = remove_trailing_whitespace(content)
    
    assert isinstance(ret, str)
    assert expected == ret


"""
test a normal metablock
test a metablock with attributes attached
test empty meta block
test incorrectly formatted metablock
test non unique meta keys
"""
def test_process_meta_block_empty():
    content = [
        "---",
        "---",
    ]
    content = "\n".join(content)
    expected = {}
    
    ret = process_meta_block(content)
    
    # test correct return value
    assert isinstance(ret, dict)
    assert expected == ret
    

def test_process_meta_block_normal():
    content = [
        "---",
        "title: test title",
        "author: firstname lastname",
        "tags: tag1,tag2,tag3",
        "---",
    ]
    
    content = "\n".join(content)
    
    expected = {
        "title": "test title",
        "author": "firstname lastname",
        "tags": "tag1,tag2,tag3",
    }
    
    ret = process_meta_block(content)
    
    # test correct return value
    assert isinstance(ret, dict)
    assert expected == ret
    
def test_process_meta_block_with_props():
    content = [
        "---",
        "title: test title",
        "author: firstname lastname",
        "tags: tag1,tag2,tag3",
        "---",
        "{ blocktype='meta' }",
    ]
    content = "\n".join(content)
    
    expected = {
        "blocktype": "meta",
        "title": "test title",
        "author": "firstname lastname",
        "tags": "tag1,tag2,tag3",
    }
    
    ret = process_meta_block(content)
    
    # test correct return value
    assert isinstance(ret, dict)
    assert expected == ret


def test_process_meta_block_non_unique_keys():
    """
    when converting a tuple pair into a dict, 
    non-unique values are just updated in the dict
    """
    content = [
        "---",
        "title: test title 1",
        "title: test title 2",
        "author: firstname lastname",
        "tags: tag1,tag2,tag3",
        "---",
    ]
    content = "\n".join(content)
    
    expected = {
        "title": "test title 2",
        "author": "firstname lastname",
        "tags": "tag1,tag2,tag3",
    }
    
    ret = process_meta_block(content)
    
    # test correct return value
    assert isinstance(ret, dict)
    assert expected == ret
    
