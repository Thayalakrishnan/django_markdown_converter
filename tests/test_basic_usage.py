from django_markdown_converter.blockify import Blockify
from django_markdown_converter.helpers.helpers import ReadSourceFromFile, ReadJSONFromFile
from pathlib import Path
import os

def test_blockifier_creation():
    
    md = """
    # Heading 1
    
    This is a paragraph after a heading. 
    
    """

    output = Blockify(md)
    assert isinstance(output, list)


def test_basic_usage_from_source():
    path_to_file = "tests/examples/post.md"
    path_to_json = "tests/examples/post.json"
    md = ReadSourceFromFile(path_to_file)
    output_expected = ReadJSONFromFile(path_to_json)
    output = Blockify(md)
    assert isinstance(output, list)
    assert isinstance(output_expected, list)
    
    for o, o_e in zip(output, output_expected):
        assert o["type"] == o_e["type"]
    

