import pytest

#from django.base_blockifier import BaseBlockifier
#from django_markdown_converter.blockifiers.base_blockifier import BaseBlockifier
from django_markdown_converter.blockifiers.blocks.base import BaseBlockifier


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
        pattern=r'^(?P<content>.*?)$',
        name="everything",
        left="",
        right="",
        singleline=False,
        nested=False,
        priority=100,
        nestedpriority=0,
    )


def test_base_blockifier(my_class_instance):
    assert 1 > 2

def test_base_priority(my_class_instance):
    assert 1 > 2

def test_base_create_block(my_class_instance):
    assert 1 > 2

def test_base_create_chunk(my_class_instance):
    assert 1 > 2

def test_base_get_type(my_class_instance):
    assert 1 > 2

def test_base_get_props(my_class_instance):
    assert 1 > 2

def test_base_get_data(my_class_instance):
    assert 1 > 2

def test_base_get_matched_group(my_class_instance):
    assert 1 > 2

def test_base_get_attrs(my_class_instance):
    assert 1 > 2

def test_base_reset_bank(my_class_instance):
    assert 1 > 2

def test_base_get_bank(my_class_instance):
    assert 1 > 2

def test_base_blockify(my_class_instance):
    assert 1 > 2