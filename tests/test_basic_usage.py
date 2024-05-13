from django_markdown_converter.blockify import Blockify


def test_blockifier_creation():
    
    md = """
    # Heading 1
    
    This is a paragraph after a heading. 
    
    """
    output = Blockify(md)
    assert isinstance(output, list)

def test_basic_usage():
    
    md = """
    # Heading 1
    
    This is a paragraph after a heading. 
    
    """
    output = Blockify(md)
    assert isinstance(output, list)
