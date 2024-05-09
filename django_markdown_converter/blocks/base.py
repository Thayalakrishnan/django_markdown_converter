import re
from typing import Literal

class BaseBlockifier:

    PATTERN_ATTRS = re.compile(r'\s*(?P<key>\S+)\=\"(?P<value>.*?)\"', re.DOTALL)
    
    __slots__ = ("pattern", "name", "left", "right", "flagged", "bank", "singleline", "nested", "priority", "nestedpriority",)

    def __init__(
        self,
        pattern:Literal[r'']=r'',
        name:str="",
        left:str="",
        right:str="",
        singleline:bool=False,
        nested:bool=False,
        priority:int=0,
        nestedpriority:int=0,
         *args,
        **kwargs
        ) -> None:

        self.pattern = re.compile(pattern, re.MULTILINE | re.DOTALL)
        self.name = name
        self.left = left
        self.right = right
        self.flagged = False
        self.singleline = singleline
        self.nested = nested
        self.priority = priority
        self.nestedpriority = nestedpriority
        self.bank = []

        self.setUp(*args, **kwargs)

    def setUp(self, *args, **kwargs) -> None:
        """override this method to do additional setup outside of the init"""
        pass

    def blockify(self, lines:list=[]) -> dict:
        """takes lines and return a block"""
        chunk = self.createChunk(lines)
        match = self.pattern.search(chunk)
        if match:
            self.flagged = True
            return self.createBlock(match=match, lines=lines, chunk=chunk)
        return {}

    def createBlock(self, *args, **kwargs) -> dict:
        '''
        create the block by extract the content
        we then split the content into lines and then
        split again by the colon sperator
        this gives us the key value pairs
        '''
        props = self.getProps(*args, **kwargs)
        kwargs.update({"props": props})
        data = self.getData(*args, **kwargs)

        block = {
            "type": self.getType(*args, **kwargs),
            "props": props,
            "data": data
        }
        self.bank.append(block)
        return block

    def createChunk(self, lines:list=[]) -> str:
        """take the lines passed in and make it into a chunk we can match against"""
        return "\n".join(lines)

    def getType(self, *args, **kwargs):
        """return the block name. we can override this if we need to change the name"""
        return self.name


    def getProps(self, match, *args, **kwargs):
        """return the attributes as properties of the block"""
        if match.group('attrs'):
            return self.getAttrs(match.group('attrs'))
        return {}

    def getData(self, match, *args, **kwargs):
        """return the matched content as the data for the block"""
        if match.group('content'):
            return match.group('content')
        return ""

    def get_matched_group(self, match, name, default):
        """given a labelled match group, return the data"""
        if match.group(name):
            return match.group(name)
        return default

    def getAttrs(self, line):
        """get the attributes"""
        props = {}
        # extract the attrs from the given line
        match_attrs = self.PATTERN_ATTRS.findall(line)

        if match_attrs:
            props.update(dict(match_attrs))

        return props

    def resetBank(self):
        self.flagged = False
        self.bank = []

    def getBank(self):
        return self.bank