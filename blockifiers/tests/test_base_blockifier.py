import pytest

from ..base_blockifier import BaseBlockifier

TEST_DATA = {
    "pattern": r'^(?P<content>.*?)$)',
    "name": "everything",
    "priority": 100,
    "left": "",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0
}


@pytest.fixture
def my_class_instance():
    return BaseBlockifier(
        pattern=r'^(?P<content>.*?)$)',
        name="everything",
        left="",
        right="",
        singleline=False,
        nested=False,
        priority=100,
        nestedpriority=0,
    )


def test_base_blockifier(obj):
    assert False

def test_base_priority(obj):
    assert False

def test_base_createBlock(obj):
    assert False

def test_base_createChunk(obj):
    assert False

def test_base_getType(obj):
    assert False

def test_base_getProperties(obj):
    assert False

def test_base_getData(obj):
    assert False

def test_base_get_matched_group(obj):
    assert False

def test_base_getAttrs(obj):
    assert False

def test_base_resetBank(obj):
    assert False

def test_base_getBank(obj):
    assert False

def test_base_blockify(obj):
    assert False