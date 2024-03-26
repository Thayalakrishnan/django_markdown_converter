import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


print(sys.path)
print(os.path)

import pytest
from src.django_markdown_converter.blockify import Blockify


def test_basic_usage():
    
    md = """
    # Heading 1
    
    This is a paragraph after a heading. 
    
    """
    output = Blockify(md)
    assert isinstance(output, list)
