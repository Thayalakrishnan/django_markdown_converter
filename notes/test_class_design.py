# %%
"""
see if we can add the instance creations to a shared bank
so that we can auto keep track of all the patterns
that have been subclasses on creation
"""

# %%

class Pattern:
    BLOCKS = []
    LOOKUP = {}
    
    def __init__(self, name:str="") -> None:
        self.name = name
        self.count = 0
        self.LOOKUP.update({self.name: self})
    
    def create_block(self):
        self.count+=1
        block = {"type": self.name, "index": self.count}
        self.BLOCKS.append(block)
        return block

    def __repr__(self) -> str:
        return self.name
    
    #@property
    @classmethod
    def get_instances(cls):
        return list(cls.LOOKUP.values())

    @classmethod
    def create_blocks(cls):
        instances = cls.LOOKUP.values()
        for _ in instances:
            _.create_block()

class TablePattern(Pattern):
    def __init__(self) -> None:
        super().__init__("table")

class CodePattern(Pattern):
    def __init__(self) -> None:
        super().__init__("code")

class ListPattern(Pattern):
    def __init__(self) -> None:
        super().__init__("list")


TablePattern()
#CodePattern()

#print(code_pat.BANK)
print(Pattern.BLOCKS)
print(Pattern.get_instances())

#for _ in Pattern.get_instances():
#    print(_.__mro__)

print(Pattern.LOOKUP)
print(Pattern.__subclasses__())
Pattern.create_blocks()
print(Pattern.BLOCKS)



# %%
