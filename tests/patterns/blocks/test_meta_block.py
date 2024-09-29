import pytest
from django_markdown_converter.patterns.blocks.meta import MetaPattern

META_BLOCK_DATA = {
    "type": "meta",
    "props": {},
    "data": {
        "title": "meta block test",
        "author": "lawen t"
    }
}


META_MD_DATA = f'''---
title: {META_BLOCK_DATA["data"]["title"]}
author: {META_BLOCK_DATA["data"]["author"]}
---'''

def test_basic_conversion():
    result = MetaPattern().convert(META_MD_DATA)
    assert META_BLOCK_DATA == result

def test_basic_reversion():
    result = MetaPattern().revert(META_BLOCK_DATA)
    assert META_MD_DATA == result