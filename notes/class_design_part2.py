# %%

class Manager:
    BLOCKS = []
    LOOKUP = {}
    
    def __init__(self) -> None:
        print("New Manager")
        for pattern in Pattern.__subclasses__():
            inst = pattern(manager=Manager)
            self.LOOKUP.update({str(inst): inst})
    
    def convert(self, string:str="") -> list:
        """convert a line separated strings into a list of blocks"""
        return []
    
    def revert(self, blocks:list=[]) -> str:
        """convert a block into a string"""
        return ""
    
    def convert_block(self, string:str="") -> str:
        return ""
    
    def convert_inline(self, block:dict={}) -> str:
        return ""
    
    def revert_block(self, block:dict={}) -> str:
        return ""
    
    def revert_inline(self, block:dict={}) -> str:
        return ""


class Pattern:
    
    def __init__(self, manager:Manager=None, name:str="") -> None:
        print("New Pattern")
        self.manager = manager
        self.name = name
        self.count = 0
        
    def __repr__(self) -> str:
        return self.name

    def create_block(self):
        self.count+=1
        block = {"type": self.name, "index": self.count}
        self.BLOCKS.append(block)
        return block

    def convert(self, string:str="") -> dict:
        """convert a string into a block"""
        block = {}
        return block
    
    def revert(self, block:dict={}) -> str:
        """convert a block into a string"""
        return ""

class TablePattern(Pattern):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="table", *args, **kwargs)

class CodePattern(Pattern):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="code", *args, **kwargs)

class ListPattern(Pattern):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="list", *args, **kwargs)

class ParagraphPattern(Pattern):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="paragraph", *args, **kwargs)


pat = Manager()
print(pat.LOOKUP)
# %%
