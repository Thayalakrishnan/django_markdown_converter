import re
from django_markdown_converter.helpers.processors import convert_props, process_input_content

BLOCK_PATTERN_RAW = r'(?P<block>^(?:```.*?```.*?)|(?:.*?))(?:^\{(?P<props>.*?)\} *?$\n)?^\n' ## works

class BasePattern:
    
    PRIVATE_BANK = []
    BLOCK_LOOKUP = {}
    BLOCK_LIST = []
    BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)
    
    def __init__(self, name:str="base", pattern_object:dict={}, *args, **kwargs) -> None:
        
        self.name = name
        self.can_process_nested_blocks = False
        
        if pattern_object:
            #print(f"initialising {name}")
            self.addToLookup = pattern_object["addToLookup"]
            
            if self.addToLookup:
                self.blocktype = pattern_object["type"]
                
                self.check_pattern = re.compile(pattern_object["check"], re.MULTILINE | re.DOTALL)
                self.pattern = re.compile(pattern_object["pattern"], pattern_object["flags"])
                
                self.hasNested = pattern_object["hasNested"]
                self.hasInline = pattern_object["hasInlineMarkup"]
                
                self.props = pattern_object["props"]
                self.data = pattern_object["data"]
            
                self.match = False
                self.block = None
                self.bank = []
                self.BLOCK_LOOKUP.update({self.blocktype: self})
                self.BLOCK_LIST.append(self)
        else:
            self.InitialiseClasses()
            self.can_process_nested_blocks = True
    
    @classmethod
    def InitialiseClasses(cls) -> None:
        """collect the subclasses and initialise them"""
        for _ in cls.__subclasses__():
            _()
    
    def __repr__(self) -> str:
        return self.name
    
    def check(self, block) -> bool:
        return self.check_pattern.match(block)
    
    def update_props(self):
        for p in self.props:
            if p == "data":
                continue
            if self.match.group(p):
                self.block["props"].update({p: self.match.group(p).strip()})
            if p == "attrs":
                attrs = convert_props(self.match.group("attrs"))
                self.block["props"].update(attrs)
                del self.block["props"]["attrs"]

    def get_props(self, props:str="") -> dict:
        if props:
            return convert_props(props)
        return {}
    
    def get_match(self, content):
        self.match = self.pattern.match(content)
        
    def get_data(self) -> dict:
        if "data" in self.data:
            return self.match.group("data").strip()
        return {}
    
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        """
        the props can come in as:
        - curly braced enclosed attrs, after a block elelemt
        - a string of key value pairs from something like a XML element
        """
        #print(f"converting: {self.blocktype}")
        self.get_match(content)
        if not self.match:
            return {}
        self.block = {
            "type": self.blocktype,
            "props": self.get_props(props),
            "data": self.get_data()
        }
        self.update_props()
        self.add_to_bank()
        if self.can_process_nested_blocks and self.hasNested:
            self.block_converter(self.block)
        return self.block
    
    def add_to_bank(self, *args, **kwargs) -> None:
        if self.hasNested:
            self.bank.append(self.block)
            self.PRIVATE_BANK.append(self.block)
    
    def revert(self, block:dict={}, *args, **kwargs) -> str:
        self.block = block
        #print(f"reverting: {self.blocktype}")
        return block["data"]
    
    def lookup_revert(self, block:dict={}) -> str:
        return self.BLOCK_LOOKUP[block["type"]].revert(block)
    
    def lookup_convert(self, content:str="") -> dict:
        con = list(self.block_parser(process_input_content(content)))
        if len(con) > 1:
            print(con)
            return con
        return [content]


    @classmethod
    def block_generator(cls, content:str=""):
        """
        generator function that loops over the content 
        and yields blocks according to the block pattern
        """
        chunks = cls.BLOCK_PATTERN.finditer(content)
        for index, chunk in enumerate(chunks):
            block = chunk.group("block")
            props = chunk.group("props")
            if block:
                yield block, props, index

    @classmethod
    def block_detector(cls, block:str="", props:str="", index:int=0) -> dict:
        """
        receives a 'block' and determinest the type
        of block content using the block patterns list. 
        """
        for pattern in cls.BLOCK_LIST:
            if pattern.check(block):
                return pattern.convert(block, props)

    @classmethod
    def block_parser(cls, content:str=""):
        """
        from the content, loop over it to create blocks
        return an object that indicates the blocks
        index, the type of block, the content extracted 
        and any props
        """
        blocks = cls.block_generator(content)
        for block, props, index in blocks:
            yield cls.block_detector(block, props, index)
            
    @classmethod
    def block_converter(cls, block:dict={}) -> dict:
        """
        take a block as input and convert its "data" key form md to blocks
        """
        blocks = []
        source = process_input_content(block["data"])
        print(source)
        for b in cls.block_parser(source):
            #print(f"converting: {b['type']}")
            if b:
                blocks.append(b)
        if len(blocks):
            block["data"] = blocks
            
    @classmethod
    def convert_md_to_json(cls, md:str="") -> dict:
        """
        take a block as input and convert its "data" key form md to blocks
        """
        root = {"type": "root", "data": md}
        cls.block_converter(root)
        return root["data"]
    
    @classmethod
    def block_reverter(cls, blocklist:list=[]):
        for block in blocklist:
            string = cls.BLOCK_LOOKUP[block["type"]].revert(block)
            yield string
        
    @classmethod
    def convert_json_to_md(cls, blocks:list=[]) -> str:
        """
        take a block as input and convert its "data" key form md to blocks
        """
        strings = []
        for string in cls.block_reverter(blocks):
            strings.append(string)
        return "\n\n".join(strings) + "\n"
    
    @classmethod
    def tokenize(cls, content:str=""):
        chunks = cls.BLOCK_PATTERN.finditer(content)
        for index, chunk in enumerate(chunks):
            block = chunk.group("block")
            props = chunk.group("props")
            if block:
                for pattern in cls.BLOCK_LIST:
                    if pattern.check(block):
                        yield pattern.name, block
                        break

from django_markdown_converter.patterns.blocks import *
    