# %%
"""
i want to see if its okay to edit a string that is stored in list and return
an object in its place in that list. 
"""

blocklist = [
    {
        "type": "paragraph",
        "props": {},
        "data": [
            "this is some raw stuff in this paragraph. ",
            {
                "tag": "text",
                "data": "Pargraph 1 "
            },
            {
                "tag": "strong",
                "data": "with"
            },
            {
                "tag": "text",
                "data": " inline markup!"
            },
            "this is some more raw stuff at the end. ",
        ]
    }
]

print("stage 1")
for block in blocklist:
    subblockdata = block["data"]
    for subb in range(len(subblockdata)):
        print(subblockdata[subb])


print("stage 2")
for block in blocklist:
    subblockdata = block["data"]
    for subb in range(len(subblockdata)):
        if isinstance(subblockdata[subb], str):
            subblockdata[subb] = {"type": "text", "data": subblockdata[subb]}
        
print("stage 3")
for block in blocklist:
    subblockdata = block["data"]
    for subb in range(len(subblockdata)):
        print(subblockdata[subb])
            
print("done!")
# %%
"""
i want to see if its okay to edit a string that is stored in list and return
an object in its place in that list. 
"""

sentences = [
    "sentence 1",
    "sentence 2",
    "sentence 3",
    "sentence 4",
]

blocklist = [
    {
        "type": "paragraph",
        "props": {},
        "data": sentences[0]
    },
    {
        "type": "paragraph",
        "props": {},
        "data": sentences[1]
    },
    {
        "type": "paragraph",
        "props": {},
        "data": sentences[2]
    },
    {
        "type": "paragraph",
        "props": {},
        "data": sentences[3]
    },
]


print("stage 1")
for sentence in sentences:
    print(sentences)

print("stage 2")
for index, sentence in enumerate(sentences):
    sentences[index] = {"data": sentence + " yeet!"}
        
print("stage 3")
for sentence in sentences:
    print(sentences)

print("done!")

# %%
"""
see if we can add the instance creations to a shared bank
so that we can auto keep track of all the patterns
that have been subclasses on creation
"""

# %%
class Pattern:
    
    def __new__(cls):
        print("New Pattern")
        return super().__new__(cls)
    
    def __init__(self, name:str="") -> None:
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
        """
        receive a string object / convert it back into an object
        """        
        block = {}
        return block
    
    def revert(self, block:dict={}) -> str:
        """
        receive a block object
        convert it back into a markdown string
        """
        return ""


class TablePattern(Pattern):
    def __init__(self) -> None:
        super().__init__("table")

class CodePattern(Pattern):
    def __init__(self) -> None:
        super().__init__("code")

class ListPattern(Pattern):
    def __init__(self) -> None:
        super().__init__("list")

class ParagraphPattern(Pattern):
    def __init__(self) -> None:
        super().__init__("paragraph")


class Manager:
    BLOCKS = []
    LOOKUP = {}
    
    def __new__(cls):
        print("New Manager")
        return super().__new__(cls)
    
    def __init__(self) -> None:
        for pattern in Pattern.__subclasses__():
            inst = pattern()
            self.LOOKUP.update({str(inst): inst})
    
    def convert(self, string:str="") -> list:
        """
        receive a string
        convert it into a list of block object
        """
        return ""
    
    def revert(self, blocks:list=[]) -> str:
        """
        receive a list of block objects
        convert them into a string
        """
        return ""
    
    def convert_block(self, string:str="") -> str:
        """
        """
        return ""
    
    def convert_inline(self, block:dict={}) -> str:
        """
        """
        return ""
    
    def revert_block(self, block:dict={}) -> str:
        """
        """
        return ""
    
    def revert_inline(self, block:dict={}) -> str:
        """
        """
        return ""

#print(code_pat.BANK)
#Pattern()
yeet = Pattern.__subclasses__()
for _ in yeet:
    print(repr(_))

pat = Manager()
print(pat.LOOKUP)
# %%
