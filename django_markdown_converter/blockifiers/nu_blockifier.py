import re

from django_markdown_converter.helpers.processors import process_input_content, extract_metablock, process_props
from django_markdown_converter.helpers.parsers import block_parser

"""
edge cases
- rogue spacing
- rogue attrs for blocks
"""

TAB_LENGTH = 4

META_BLOCK_DATA = r'^---\s*\n(?P<content>.*?)\n\s*---\s*(?:\n\s*|$)'
UNORDERED_LIST_BLOCK_DATA = r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)'
ORDERED_LIST_BLOCK_DATA = r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)'
DEFINITIONLIST_BLOCK_DATA = r'^\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$)'
FOOTNOTE_BLOCK_DATA = r'\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)'
ADMONITION_BLOCK_DATA = r'!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)'
CODE_BLOCK_DATA = r'(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<content>.*?)(?<=\n)(?P<stop>(?:```))\s*'
TABLE_BLOCK_DATA = r'^(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n|\|$))+)(?:(?:\{\s*(?P<attrs>.*?)\s*\})?)'
BLOCKQUOTE_BLOCK_DATA = r'(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<content>(?:\>\s+.*(?:\n|$))+)'
HR_BLOCK_DATA = r'^\s*(?P<content>\*\*\*)\s*(?:\n|$)'
HEADING_BLOCK_DATA = r'^(?P<level>#{1,6})\s+(?P<content>.*?)(?:\{(?P<attrs>.*?)\})?\s*(?:\n|$)'
IMAGE_BLOCK_DATA = r'!\[(?P<attrs>.*?)\]\((?P<content>.*?)\)'
PARAGRAPH_BLOCK_DATA = r'(?P<content>.*?)(?:\n|$)(?P<after>.*?)'

SVG_BLOCK_DATA = r'^<svg (?P<attrs>[^>]*)>(?P<between>.*?)</svg>(?P<after>.*)$'
PARAGRAPH_BLOCK_DATA = r'^(?P<content>.*?)(?:\n\n)(?P<after>.*?)$'

def process_input_content(content:str=""):
    """
    homogenise the content so we always have the correct
    inputs
    """
    pass


def process_chunk(chunk):
    # receive chunk
    # extract attrs
    return

def find_next(content:str="", patterns:list=[]):
    """
    generator that goes to work finding the next block
    it will yield the block
    """
    raw_pattern = r'(?P<chunk>```.*?```|.*?)\n\n'
    pattern = re.compile(raw_pattern, re.MULTILINE | re.DOTALL)
    match = pattern.finditer(content)

    for index, m in enumerate(match):
        chunk = m.group("chunk")
        for pat in patterns:
            submatch = pat.match(chunk)



def blockify(content:str=""):
    """
    """
    root = {"type": "root", "meta": None, "children": []}

    # process content
    ## strip whitespace and ensure correct block spacing
    processed_content = process_input_content(content)

    # extract meta block
    processed_content, meta = extract_metablock(processed_content)
    root["meta"] = meta

    # loop over blocks and create first pass of block elements
    for index, label, content, props in block_parser(processed_content):
        root["children"].append({
            #"index": index,
            "blocktype": label,
            "props": process_props(props),
            "data": content
        })
    ## ensure any footnotes encountered are added to the back and not the
    ## flow, we can also do this last after the first pass
    # loop over elements that may nested block level elements
    # convert inline markup
    pass