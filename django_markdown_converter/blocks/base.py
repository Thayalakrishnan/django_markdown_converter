import re
from typing import Literal

"""
pattern: r'^---\s*\n(?P<content>.*?)\n\s*---\s*(?:\n\s*|$)'
name: "base"
left: "---"
right: "---"
flagged: False
singleline: False
nested: False
priority: 10
nestedpriority: 0
"""

class BaseBlockifier:

    PATTERN_ATTRS = re.compile(r'\s*(?P<key>\S+)\=\"(?P<value>.*?)\"', re.DOTALL)
    
    __slots__ = ("pattern", "name", "left", "right", "flagged", "bank", "singleline", "nested", "priority", "nestedpriority",)

    def __init__(
        self,
        pattern:Literal[r'']=r'',
        name:str="",
        left:str="",
        right:str="",
        flagged:bool=False,
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
        self.flagged = flagged
        self.singleline = singleline
        self.nested = nested
        self.priority = priority
        self.nestedpriority = nestedpriority
        self.bank = []

        self.setUp(*args, **kwargs)

    def setUp(self, *args, **kwargs) -> None:
        """override this method to do additional setup outside of the init"""
        pass
    
    def test_lines(self, *args, **kwargs) -> None:
        """use this method to test the block"""
        pass

    def blockify(self, lines:list=[]) -> dict:
        """takes lines and return a block"""
        chunk = self.create_chunk(lines)
        match = self.pattern.search(chunk)
        if match:
            self.flagged = True
            return self.create_block(match=match, lines=lines, chunk=chunk)
        return {}

    def create_block(self, *args, **kwargs) -> dict:
        """
        create the block by extract the content
        we then split the content into lines and then
        split again by the colon sperator
        this gives us the key value pairs
        """
        props = self.get_props(*args, **kwargs)
        kwargs.update({"props": props})
        data = self.get_data(*args, **kwargs)

        block = {
            "type": self.get_type(*args, **kwargs),
            "props": props,
            "data": data
        }
        self.bank.append(block)
        return block
    
    #@staticmethod
    def create_chunk(self, lines:list=[]) -> str:
        """take the lines passed in and make it into a chunk we can match against"""
        return "\n".join(lines)

    def get_type(self, *args, **kwargs):
        """return the block name. we can override this if we need to change the name"""
        return self.name


    def get_props(self, match, *args, **kwargs):
        """return the attributes as properties of the block"""
        if match.group('attrs'):
            return self.get_attrs(match.group('attrs'))
        return {}

    def get_data(self, match, *args, **kwargs):
        """return the matched content as the data for the block"""
        if match.group('content'):
            return match.group('content')
        return ""

    def get_matched_group(self, match, name, default):
        """given a labelled match group, return the data"""
        if match.group(name):
            return match.group(name)
        return default

    def get_attrs(self, line):
        """get the attributes"""
        props = {}
        # extract the attrs from the given line
        match_attrs = self.PATTERN_ATTRS.findall(line)

        if match_attrs:
            props.update(dict(match_attrs))

        return props

    def reset_bank(self):
        self.flagged = False
        self.bank = []

    def get_bank(self):
        return self.bank