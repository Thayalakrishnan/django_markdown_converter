from django_markdown_converter.blockifiers.blockifier import BIG_BLOCKIFIER

from django_markdown_converter.helpers.processors import process_input_content, extract_meta_block
from django_markdown_converter.helpers.parsers import block_parser, nested_blocks_parser


'''
edge cases
- with list, ordered, table, blockquote, there are edge cases
where it just so happens that that pattern is at the beggining of a string

find the end of the line, which should
be an empty line (len(line) == 0)
the reason we need to add a one here is because of
list slicing, where the second argument is exclusive and
not inclusive like the first argument. therefore,
when we are working with a block which has defined opening and
closing boundaries (not just a black string), we need to ensure
we capture this.

becuase codeblocks can have empty lines within them, we need
to ensure we are going all the way to the end fence of the code block.
here, we see if the boundary has a length, in which case we do ensure
we go past the fence. Most of the blocks end on a new empyty line, so
the length of their boundary is 0.
'''

def Blockify(source:str=""):
    return BIG_BLOCKIFIER.run_blockify(source)


def Convert(source:str="") -> list:
    """
    receive a string, presumably formatted
    using markdown
    convert the markdown into our json format
    and return this object
    """
    blocks = []
    source = process_input_content(source)
    for block in block_parser(source):
        blocks.append(block)
    while nested_blocks_parser():
        continue
    return blocks


def Revert(source:list=[]) -> str:
    """
    receive a list of blocks that represent
    string in markdown formatting
    converting the blocks into markdown
    return the blocks as the markdown string form
    """
    return ""

