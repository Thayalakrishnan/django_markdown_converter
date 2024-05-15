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
    OrderedListBlockifier,
    UnOrderedListBlockifier,
    DefinitionListBlockifier,
    SVGBlockifier,
]

class Blockifier:

    def __init__(self):
        self.blockifiers = []
        self.nested_blockifiers = []
        self.lookup_blockifier = {} # lookup for all blocks
        
        self.build_blockifiers(BLOCKIFIER_DATA)
        
        self.default_blockifier = self.get_blockifier_with_key("paragraph")

#   this is the old build function i had
#    def build_blockifiers(self, setup_data:list=[]) -> None:
#        for block_data in setup_data:
#            key = block_data["name"]
#            blockifier = block_data["class"](**block_data)
#            setattr(self, key, blockifier)
#            self.blockifiers.append(blockifier)
#            self.lookup_blockifier[key] = blockifier
#            if blockifier.nested:
#                self.nested_blockifiers.append(blockifier)
#        self.blockifiers.sort(key=lambda x: x.priority)
#        self.nested_blockifiers.sort(key=lambda x: x.nestedpriority)
        
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

    def find_next_block(self, lines:list=[], index_max:int=1) -> tuple:
        #print(f"find_next_block")
        # loop until we find the start of a viable line
        #index_max = len(lines)
        for index_start in range(index_max - 1):
            # if the line is empty, move to next line
            if not len(lines[index_start]):
                continue

            # boundary test loops over all the boundaries we have
            # and determines which boundary it is
            for blockifier in self.blockifiers:
                #if blockifier.name == "paragraph":
                #    print(f"blockifier: {blockifier.name}")

                if lines[index_start].startswith(blockifier.left):
                    # once we find the boundary, we look for the closing boundary 
                    # so increase the current index
                    for index_stop in range(index_start+1, index_max):
                        
                        if lines[index_stop] == blockifier.right:
                            #print(f"block lines: {index_start} - {index_stop}")
                            #print(lines[index_start:index_stop])

                            # if the line here is empty, we slice here
                            if not len(lines[index_stop]):
                                return self.extract_block(blockifier, lines, index_start, index_stop)

                            # if not we slice at the next index
                            return self.extract_block(blockifier, lines, index_start, index_stop + 1)

        return self.extract_block(self.default_blockifier, lines, 0, index_max)
    
    def new_find_next_block(self, lines:list=[], index_max:int=1) -> tuple:
        for index_start in range(index_max - 1):
            # skip lines that are empty
            if not len(lines[index_start]):
                continue
            for blockifier in self.blockifiers:
                chunk = "\n".join(lines[index_start::])
                match = blockifier.pattern.match(chunk)
                if match:
                if lines[index_start].startswith(blockifier.left):
                    for index_stop in range(index_start+1, index_max):
                        if lines[index_stop] == blockifier.right:
                            if not len(lines[index_stop]):
                                return self.extract_block(blockifier, lines, index_start, index_stop)
                            return self.extract_block(blockifier, lines, index_start, index_stop + 1)
                        
        return self.extract_block(self.default_blockifier, lines, 0, index_max)
    
    def find_blocks(self, lines:list=[]):
        #print(f"find_blocks")
        """loop over the lines to detect blocks"""
        pos_cur = 0
        pos_max = len(lines)

        while pos_cur < pos_max:
            new_block, index_c = self.find_next_block(lines[pos_cur:], pos_max - pos_cur)

            # sometimes a block will return negative, so check for that
            if new_block:
                if type(new_block) == list:
                    for _ in new_block:
                        yield _
                else:
                    yield new_block

            # adjust the current position
            pos_cur = pos_cur + index_c

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
            #print(f"block: {b['type']}")
            block_list.append(b)
        return block_list

    def run_blockify(self, source:str="") -> list:
        #print(f"run_blockify")
        self.reset_nested_banks()
        block_list = self.blockify(source)
        self.process_nested_blockifiers()
        self.add_footnotes(block_list)
        return block_list


BIG_BLOCKIFIER = Blockifier()
