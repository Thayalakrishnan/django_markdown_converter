import pytest
from django_markdown_converter.helpers.parsers import block_parser
from django_markdown_converter.helpers.helpers import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content, extract_attrs, extract_meta_block

def extract_solution(path):
    raw_sol = ReadSourceFromFile(path)
    raw_sol = raw_sol.strip(" \n")
    raw_sol = raw_sol.split("\n")
    ret = []
    for entry in raw_sol:
        ret.append(str(entry))
    return ret


def test_block_parser():
    """
    this obviously needs to be fixed
    we are doing too much before actually testing our block parser
    """
    path_to_solution = "notes/examples/post_answer.md"
    solution = extract_solution(path_to_solution)
    
    path_to_file = "notes/examples/post.md"
    raw_chunk = ReadSourceFromFile(path_to_file)
    raw_chunk = process_input_content(raw_chunk)
    raw_chunk, meta = extract_meta_block(raw_chunk)
    
    for index, label, content, attrs in block_parser(raw_chunk):
        assert solution[index] == label
