#%%

class TokenValue:
    STACK = []
    """
    base token class
    cases:
    - need to iknow if the value i sopen or closed
    - need to know if the value is encased so that we can sum them 
    """
    #__slots__ = ['name', 'depth', 'value', 'index',]
    __slots__ = ['name', 'depth', 'value',]
    
    def __init__(self, name:str="", depth:int=0, value:str=""):
        self.name = name
        self.depth = depth
        self.value = value

    
    def __repr__(self):
        #return f"{self.name}"
        return f"{self.value}"
    
    def __eq__(self, other):
        #return self.name == other.name and type(self.value) == type(other.value) 
        return type(self) == type(other) and self.name == other.name
    
    def __gt__(self, other):
        return self.depth > other.depth
    
    def __lt__(self, other):
        return self.depth < other.depth


"""
linear tokens: do not nest and contain all the infor right there
nesting tokens: contain their own stack
root token: contains everything
- linear1 + linear2 = linear1 + linear2 <nothing>
- linear1 + linear1 = linear1.value += linear1.value
"""
class NestingToken(TokenValue):
    """
    nesting token
    - nesting1 + linear1 = nesting1.root.append(linear1) | current_root.root.append(linear1) 
    - nesting1 + nesting2 = stack.append(nesting1) -> current_root = nesting2
    - nesting1[O] + nesting1[C] = current_root = stack.pop() -> new root
    - nesting1[O] + nesting2[O] + nesting1[C] = <error> stack.pop() -> nesting1.extend(nesting2.root)
    """
    TRACKER = {}
    __slots__ = ['name', 'depth', 'value', 'root', 'stack', 'base', 'parent', 'is_open']
    
    def __init__(self, name:str="", depth:int=0, value:str=""):
        super().__init__(name, depth, value)
        self.root = []
        self.base = self.root
        if name not in self.TRACKER:
            self.TRACKER[name] = False
        self.TRACKER[name] = not self.TRACKER[name]
        self.is_open = self.TRACKER[name]
        self.parent = self
    
    def __add__(self, other):
        if self < other:
            # nest the other in us
            print("nesting")
            self.STACK.append((self.root, self.depth))
            new_root = [other]
            self.root.append(new_root)
            self.root = new_root
            self.depth = other.depth
            return self
        elif self > other:
            # nest us in the other
            print("de-nesting")
            self.root, self.depth = self.STACK.pop()
            return self + other
        elif self == other:
            print("equals")
            self.root.append(other)
            return self + other
        else:
            print("other")
            self.root.append(other)
            #del other
            return self

class RootValue(TokenValue):
    """
    root class inherits from token class
    we use this class for the first element
    """
    __slots__ = ['name', 'depth', 'value', 'root', 'stack', 'base']
    
    def __init__(self):
        super().__init__(name="root", depth=0, value="")
        #self.STACK = []
        self.root = []
        self.base = self.root
    
    def __add__(self, other):
        if self < other:
            # nest the other in us
            print("nesting")
            self.STACK.append((self.root, self.depth))
            new_root = [other]
            self.root.append(new_root)
            self.root = new_root
            self.depth = other.depth
            return self
        elif self > other:
            # nest us in the other
            print("de-nesting")
            self.root, self.depth = self.STACK.pop()
            return self + other
        elif self == other:
            print("equals")
            self.root.append(other)
            return self + other
        else:
            print("other")
            self.root.append(other)
            #del other
            return self



#%%

"""
before **in _nested `double nested` content_ between** after
"""
#tv0 = RootValue()
#tv0 + TokenValue("text", 1, "this is the start")
#tv0 + TokenValue("inside", 3, " this is outside middle ")
#tv0 + TokenValue("further", 5, " inside middle ")
#tv0 + TokenValue("text", 1, "this is the end")
#tv0 + TokenValue("inside", 3, " second middle ")
#tv0 + TokenValue("further", 5, " third middle ")

tv0 = RootValue()
tv0 + TokenValue("text", 1, "this is the first level ")
tv0 + TokenValue("strong", 3, "**")
tv0 + TokenValue("text", 3, " this is the second level ")
tv0 + TokenValue("em", 5, "_")
tv0 + TokenValue("text", 5, " this is the third level ")
tv0 + TokenValue("em", 5, "_")
tv0 + TokenValue("text", 3, " continueing the second level ")
tv0 + TokenValue("code", 5, " this is a new third level ")
tv0 + TokenValue("text", 3, " back to the second level ")
tv0 + TokenValue("strong", 3, "**")
tv0 + TokenValue("text", 1, " this is the end of the first level")

#tv1 + tv2 + tv3 + tv4
#tv0 + tv1 + tv2 + tv3 + tv4 + tv5 + tv6
#print(tv0.base)
#tv0 + tv2
#print(tv0.base)
#tv0 + tv3
#print(tv0.base)
#tv0 + tv4
#print(tv0.base)
#tv0 + tv5
#print(tv0.base)
#tv0 + tv6
print(tv0.base[0])

print("done")
            
# %%
