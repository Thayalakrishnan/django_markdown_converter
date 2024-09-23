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

class ParagraphPattern(Pattern):
    def __init__(self) -> None:
        super().__init__("paragraph")


TablePattern()
CodePattern()
ListPattern()
ParagraphPattern()

#print(code_pat.BANK)
print(Pattern.BLOCKS)
print(Pattern.get_instances())

print(Pattern.LOOKUP)
print(Pattern.__subclasses__())
Pattern.create_blocks()
print(Pattern.BLOCKS)



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
