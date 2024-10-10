#%%

class TokenValue:
    __slots__ = ['name', 'depth', 'value', 'index',]
    
    def __init__(self, name:str="", depth:int=0, value:str="", index:int=0):
        self.name = name
        self.depth = depth
        self.value = value
        self.index = index
    
    def __repr__(self):
        return f"{self.name}-{self.index}"
    
    def __eq__(self, other):
        return self.name == other.name and type(self.value) == type(other.value) 
    
    def __gt__(self, other):
        return self.depth > other.depth
    
    def __lt__(self, other):
        return self.depth < other.depth
    
    #def __add__(self, other):
    #    if self < other:
    #        # nest the other in us
    #        print("nesting")
    #        self.stack.append((self.root, self.depth))
    #        new_root = [other]
    #        self.root.append(new_root)
    #        self.root = new_root
    #        self.depth = other.depth
    #        return self
    #    elif self > other:
    #        print("de-nesting")
    #        # nest us in the other
    #        self.root, self.depth = self.stack.pop()
    #        return self + other
    #    #elif self == other:
    #    #    self.value = self.value + other.value
    #    #    del other
    #    #    return self
    #    else:
    #        print("equals")
    #        self.root.append(other)
    #        #del other
    #        return self

class RootValue(TokenValue):
    __slots__ = ['name', 'depth', 'value', 'root', 'index', 'stack', 'base']
    
    def __init__(self):
        super().__init__(name="root", depth=0, value="", index=0)
        self.stack = []
        self.root = []
        self.base = self.root
    
    def __add__(self, other):
        if self < other:
            # nest the other in us
            print("nesting")
            self.stack.append((self.root, self.depth))
            new_root = [other]
            self.root.append(new_root)
            self.root = new_root
            self.depth = other.depth
            return self
        elif self > other:
            print("de-nesting")
            # nest us in the other
            self.root, self.depth = self.stack.pop()
            return self + other
        #elif self == other:
        #    self.value = self.value + other.value
        #    del other
        #    return self
        else:
            print("equals")
            self.root.append(other)
            #del other
            return self

"""
before **in _nested `double nested` content_ between** after
"""
tv0 = RootValue()
tv1 = TokenValue("text", 1, "this is the start", 1)
tv2 = TokenValue("inside", 3, " this is outside middle ", 2)
tv3 = TokenValue("further", 5, " inside middle ", 3)
tv4 = TokenValue("text", 1, "this is the end", 4)
tv5 = TokenValue("inside", 3, " second middle ", 5)
tv6 = TokenValue("further", 5, " third middle ", 6)

#tv1 + tv2 + tv3 + tv4
tv0 + tv1
print(tv0.base)
tv0 + tv2
print(tv0.base)
tv0 + tv3
print(tv0.base)
tv0 + tv4
print(tv0.base)
tv0 + tv5
print(tv0.base)
tv0 + tv6
print(tv0.stack[0])

print("done")
            
# %%
