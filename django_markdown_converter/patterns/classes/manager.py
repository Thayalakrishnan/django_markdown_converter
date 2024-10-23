import re

BLOCK_PATTERN_RAW = r'(?P<block>^(?:```.*?```.*?)|(?:.*?))(?:^\{(?P<props>.*?)\} *?$\n)?^\n' ## works


class PatternManager:
    
    PRIVATE_BANK = []
    BLOCK_LOOKUP = {}
    BLOCK_LIST = []
    
    BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)
    
    def __init__(self, *args, **kwargs) -> None:
        self.InitialiseClasses()
    
    def InitialiseClasses(self, pattern_class) -> None:
        """collect the subclasses and initialise them"""
        for _ in pattern_class.__subclasses__():
            inst = _(manager=self)
            self.BLOCK_LOOKUP.update({inst.blocktype: inst})
            self.BLOCK_LIST.append(inst)

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
    def block_reverter(cls, blocklist:list=[]):
        for block in blocklist:
            string = cls.BLOCK_LOOKUP[block["type"]].revert(block)
            yield string
            
    @classmethod
    def convert_md_to_json(cls, md:str="") -> dict:
        """
        take a block as input and convert its "data" key form md to blocks
        """
        root = {"type": "root", "data": md}
        cls.block_converter(root)
        return root["data"]
        
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