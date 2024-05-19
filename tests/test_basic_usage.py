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
    """
    here we read the example converted markdown and json files
    so that we can quickly compare if the conversions are correct
    the md file represents our markdown file
    the json file represents our expected output when 
    converting the md file
    """
    path_to_file = "tests/examples/post.md"
    path_to_json = "tests/examples/post.json"
    md = ReadSourceFromFile(path_to_file)
    blocks_expected = ReadJSONFromFile(path_to_json)
    blocks = Blockify(md)
    assert isinstance(blocks, list)
    assert isinstance(blocks_expected, list)
    
    for block, block_e in zip(blocks, blocks_expected):
        assert block["type"] == block_e["type"]
    

