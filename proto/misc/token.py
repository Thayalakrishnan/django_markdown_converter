#%%


class TokenValue:
    __slots__ = ['name', 'depth', 'value', 'root', 'root_ptr']
    
    def __init__(self, name:str="", depth:int=0, value:str="",):
        self.name = name
        self.depth = depth
        self.value = value
        self.root = [self]
        self.root_ptr = self.root
    
    def __eq__(self, other):
        return self.name == other.name and type(self.value) == type(other.value) 
    
    def __gt__(self, other):
        return self.depth > other.depth
    
    def __lt__(self, other):
        return self.depth < other.depth
                    
    def __add__(self, other):
        if self < other:
            # nest the other in us
            print("nesting")
            self.root_ptr.append(other.root)
            self.root_ptr = other.root
            #self.depth = other.depth
            return self
        elif self > other:
            print("de-nesting")
            # nest us in the other
            other.root_ptr.append(self.root)
            other.root_ptr = self.root
            #other.depth = self.depth
            return other
        #elif self == other:
        #    self.value = self.value + other.value
        #    del other
        #    return self
        else:
            self.value = self.value + other.value
            del other
            return self

"""
before **in _nested `double nested` content_ between** after
"""
         
tv1 = TokenValue("text", 1, "this is the start")
tv2 = TokenValue("inside", 3, " this is outside middle ")
tv3 = TokenValue("further", 5, " inside middle ")
tv4 = TokenValue("text", 1, "this is the end")

tv1 + tv2 + tv3 + tv4
#tv1 + tv2
#tv1 + tv3
#tv1 + tv4
print(tv1.root)
print(tv2.root)
print(tv3.root)
print(tv4.root)
            
# %%
