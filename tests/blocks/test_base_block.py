## test_base_block
import pytest
from django_markdown_converter.blocks.base import BaseBlockifier



"""
@@@ { property=value }
Block content.
@@@
"""
def create_pattern(pattern):
    start = r"^"
    left = f"^(?P<left>{pattern})"
    right = f"(?P<right>{pattern})" + r"(?:\s*\n\s*|\n\s*|$)"
    #right = f"(?P<right>{pattern})(?:\n\s*|$)"
    attrs = r"(?:\{(?P<attrs>.*?)\})?"
    wspace = r"\s*"
    nl = r"\n"
    content = r"(?P<content>.*?)"
    end = r"(?:\n\s*|$)"
    gap = r"(?:\n|\n\s*|\s*)"
    #gen_pattern=r'^@@@\s*(?:\{(?P<attrs>.*?)\})?\s*\n(?P<content>.*?)\n\s*@@@\s*(?:\n\s*|$)'
    #gen_pattern=f"{start}{left}{attrs}{gap}{content}{gap}{wspace}{right}{end}"
    #gen_pattern=f"{start}{left}{gap}{attrs}{gap}{content}{gap}{right}{end}"
    gen_pattern=f"{left}{gap}{attrs}{gap}{content}{gap}{right}"
    return gen_pattern


def create_base_blockifier():
    pattern = "@@@"
    return BaseBlockifier(
        #pattern=r'^@@@\s*(?:\{(?P<attrs>.*?)\})?\s*\n(?P<content>.*?)\n\s*@@@\s*(?:\n\s*|$)',
        #pattern=r'^@@@\s*\n(?P<content>.*?)\n\s*@@@\s*(?:\n\s*|$)',
        pattern=create_pattern(pattern),
        name="base",
        left=pattern,
        right=pattern,
        flagged=False,
        singleline=False,
        nested=False,
        priority=10,
        nestedpriority=0
    )


def test_base_init():
    blockifier = create_base_blockifier()
    block_type = "base"
    block_data = "Block content."
    block_prop_key = "property"
    block_prop_value = "value"
    
    md = [
        #"@@@ { " + f"{block_prop_key}={block_prop_value}" + " } ",
        "@@@",
        f"{block_data}",
        "@@@",
        "",
    ]
    print(md)
    output = blockifier.blockify(md)
    assert isinstance(output, dict)
    assert output != {}
    assert block_type == output["type"]
    assert block_data == output["data"]


def test_all_inline_init():
    blockifier = create_base_blockifier()
    block_type = "base"
    block_data = "Block content."
    block_prop_key = "property"
    block_prop_value = "value"
    md = [
        f'@@@ {{ yeet="yeet" }} {block_data} @@@',
        #f'@@@ {{ {block_prop_key}="{block_prop_value}" }} ',
        #f"{block_data}",
        #"@@@",
        "",
    ]
    #print(md)
    output = blockifier.blockify(md)
    print(output)
    assert isinstance(output, dict)
    assert isinstance(output, bool)
    assert output != {}
    assert block_type == output["type"]
    assert block_data == output["data"]


def test_method_blockify():
    """
    test the the blockify method returns a valid block object
    when a match is made
    """
    pass

def test_method_create_block():
    pass

def test_method_create_chunk():
    pass

def test_method_get_type():
    pass

def test_method_get_props():
    pass

def test_method_get_data():
    pass

def test_method_get_matched_group():
    pass

def test_method_get_attrs():
    pass

def test_method_reset_bank():
    pass

def test_method_get_bank():
    pass
