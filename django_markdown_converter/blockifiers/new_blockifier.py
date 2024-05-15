# blockifiers.py
#from django_markdown_converter.blockifiers.blockifier_data import BLOCKIFIER_DATA
from django_markdown_converter.blocks.admonition import AdmonitionBlockifier
from django_markdown_converter.blocks.blockquote import BlockquoteBlockifier
from django_markdown_converter.blocks.code import CodeBlockifier
from django_markdown_converter.blocks.heading import HeadingBlockifier
from django_markdown_converter.blocks.hr import HRBlockifier
from django_markdown_converter.blocks.image import ImageBlockifier
from django_markdown_converter.blocks.meta import MetaBlockifier
from django_markdown_converter.blocks.footnote import FootnoteBlockifier
from django_markdown_converter.blocks.table import TableBlockifier
from django_markdown_converter.blocks.paragraph import ParagraphBlockifier
from django_markdown_converter.blocks.list import OrderedListBlockifier, UnOrderedListBlockifier
from django_markdown_converter.blocks.definitionlist import DefinitionListBlockifier
from django_markdown_converter.blocks.svg import SVGBlockifier


BLOCKIFIER_DATA = [
    AdmonitionBlockifier,
    BlockquoteBlockifier,
    CodeBlockifier,
    HeadingBlockifier,
    HRBlockifier,
    ImageBlockifier,
    MetaBlockifier,
    FootnoteBlockifier,
    TableBlockifier,
    ParagraphBlockifier,
    #OrderedListBlockifier,
    #UnOrderedListBlockifier,
    DefinitionListBlockifier,
    SVGBlockifier,
]

class NewBlockifier:

    def __init__(self):
        self.blockifiers = []
        self.nested_blockifiers = []
        self.lookup_blockifier = {} # lookup for all blocks
        self.build_blockifiers(BLOCKIFIER_DATA)
        self.default_blockifier = self.get_blockifier_with_key("paragraph")
        
    def build_blockifiers(self, blocks:list=[]) -> None:

        for block in blocks:
            #key = block["name"]
            blockifier = block()
            key = blockifier.name

            setattr(self, key, blockifier)

            self.blockifiers.append(blockifier)
            self.lookup_blockifier[key] = blockifier

            if blockifier.nested:
                self.nested_blockifiers.append(blockifier)

        self.blockifiers.sort(key=lambda x: x.priority)
        self.nested_blockifiers.sort(key=lambda x: x.nestedpriority)

    def reset_nested_banks(self) -> None:
        for _ in self.nested_blockifiers:
            _.reset_bank()

    def extract_block(self, blockifier, lines, start, stop) -> tuple:
        """
        using the correct blockifier, we pass the lines to the blockfier 
        return a tuple containng the extracted markdown converted to a block
        and return the index after so that we know where to start from 
        """
        return (blockifier.blockify(lines[start:stop]), stop)

    def get_blockifier_with_key(self, key:str=""):
        """ return the blockifier at the given key """
        try:
            block = self.lookup_blockifier[key]
        except KeyError:
            print("blockifier does not exist")
            return False
        return block

    def process_nested_blockifiers(self) -> None:
        """ return all nested blocks that require a second parsing """
        for blockifier in self.nested_blockifiers:
            blocks = blockifier.get_bank()
            for block in blocks:
                if isinstance(block["data"], str):
                    block["data"] = self.blockify(block["data"])

    def get_meta(self, source:str=""):
        """ search source string for meta block and return only that """
        blockifier = self.get_blockifier_with_key("meta")
        if blockifier:
            return blockifier.extract_meta(source)

    def add_footnotes(self, block_list:list=[]) -> None:
        """ get the footnotes block """
        footnotes = self.get_blockifier_with_key("footnotes")
        if footnotes.flagged:
            block_list.append(footnotes.getFootnotes())
    
    def find_next_block(self, chunk:str="") -> tuple:
        #print("find_next_block")
        #print(chunk)
        for blockifier in self.blockifiers:
            
            match = blockifier.pattern.match(chunk)
            
            if match:
                #print(f"blockifier: {blockifier.name}")
                end = match.end()
                
                before = chunk[:end-1]
                after = chunk[end::].strip()
                
                block = blockifier.blockify(before.split("\n"))
                
                return (block, after)
                
        block = self.default_blockifier.blockify(chunk.split("\n"))
        return (block, "")
    
    def find_blocks(self, lines:list=[]):
        chunk = "\n".join(lines).strip()
        chunk_length = len(chunk)
        
        while chunk_length:
            print(chunk_length)
            #print("find_block generator")
            block, chunk = self.find_next_block(chunk)

            # sometimes a block will return negative, so check for that
            if block:
                if type(block) == list:
                    for _ in block:
                        yield _
                else:
                    yield block

            # adjust the current position
            if chunk_length == len(chunk):
                print("break find_blocks")
                break
            chunk_length = len(chunk)

    def convert_source_to_lines(self, source:str="") -> list:
        #print(f"convert_source_to_lines")
        """convert the source string into lines we like"""
        source = source.replace('\r', '')
        lines = source.split("\n")
        """ensure last line is empty/line broken"""
        lines.append("\n")
        return lines
            
    def blockify(self, source:str="") -> list:
        #print(f"blockify")
        block_list = []
        lines = self.convert_source_to_lines(source)
        block_gen = self.find_blocks(lines)
        for b in block_gen:
            print(f"block: {b['type']}")
            block_list.append(b)
        return block_list

    def run_blockify(self, source:str="") -> list:
        print(f"[run_blockify]")
        print(f"[run_blockify][reset_nested_banks]")
        self.reset_nested_banks()
        print(f"[run_blockify][blockify]")
        block_list = self.blockify(source)
        print(f"[run_blockify][process_nested_blockifiers]")
        self.process_nested_blockifiers()
        print(f"[run_blockify][add_footnotes]")
        self.add_footnotes(block_list)
        return block_list


NEW_BIG_BLOCKIFIER = NewBlockifier()
