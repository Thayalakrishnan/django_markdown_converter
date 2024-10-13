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
        #return type(self) == type(other) and self.name == other.name
        return self.depth == other.depth and type(self) == type(other) and self.name == other.name
    
    def __gt__(self, other):
        return self.depth > other.depth
    
    def __lt__(self, other):
        return self.depth < other.depth

class LinearToken(TokenValue):
    """
    linear tokens: do not nest and contain all the infor right there
    - linear1 + linear2 = linear1 + linear2 <nothing>
    - linear1 + linear1 = linear1.value += linear1.value
    """
    __slots__ = ['name', 'depth', 'value', 'nested', 'base', 'opening']
    pass
    
class NestingToken(TokenValue):
    """
    nesting tokens: contain their own stack
    - nesting1 + linear1 = nesting1.root.append(linear1) | current_root.root.append(linear1) 
    - nesting1 + nesting2 = stack.append(nesting1) -> current_root = nesting2
    - nesting1[O] + nesting1[C] = current_root = stack.pop() -> new root
    - nesting1[O] + nesting2[O] + nesting1[C] = <error> stack.pop() -> nesting1.extend(nesting2.root)
    """
    __slots__ = ['name', 'depth', 'value', 'nested', 'base', 'opening']
    
    def __init__(self, name:str="", depth:int=0, value:str="", opening:bool=False):
        super().__init__(name, depth, value)
        self.opening = opening
        self.base = self
        self.nested = []

    def __eq__(self, other):
        """
        they are equal if they are opposites
        """
        return super().__eq__(other) and self.opening != other.opening
    
    def nest(self, other):
        self.nested.append(other)

#%%
def add_token(a, b, stack):
    if a < b:
        # nest the other in us
        #print("nesting")
        a.nest(b)
        if isinstance(b, LinearToken):
            #print("nesting linear")
            return a
        else:
            #print("nesting nesting")
            stack.append(a)
            return b
    elif a > b:
        # nest us in the other
        #print("de-nesting")
        a = stack.pop()
        return add_token(a, b, stack)
    elif a == b:
        #print("equals")
        # if they are the same type, we can close and de-nest
        if type(a) == type(b):
            #print("equals closing")
            return stack.pop()
        else:
            #print("equals adding")
            ##print("equals")
            a.nest(b)
            return a
    else:
        #print("other")
        a.nest(b)
        return a


mystack = []
tv0 = NestingToken("root", 0, "", True)
tv0 = add_token(tv0, LinearToken("text", 1, "this is the first level "), mystack)
tv0 = add_token(tv0, NestingToken("strong", 3, "**", True), mystack)
tv0 = add_token(tv0, LinearToken("text", 3, " this is the second level "), mystack)
tv0 = add_token(tv0, NestingToken("em", 5, "_", True), mystack)
tv0 = add_token(tv0, LinearToken("text", 5, " this is the third level "), mystack)
tv0 = add_token(tv0, NestingToken("em", 5, "_", False), mystack)
tv0 = add_token(tv0, LinearToken("text", 3, " continueing the second level "), mystack)
tv0 = add_token(tv0, LinearToken("code", 5, " this is a new third level "), mystack)
tv0 = add_token(tv0, LinearToken("text", 3, " back to the second level "), mystack)
tv0 = add_token(tv0, NestingToken("strong", 3, "**", False), mystack)
tv0 = add_token(tv0, LinearToken("text", 1, " this is the end of the first level"), mystack)

def print_tokens(tokens:list=[]):
    for _ in tokens:
        if isinstance(_, NestingToken):
            print(_)
            print_tokens(_.nested)
        else:
            print(_)


print_tokens(tv0.nested)
print("done")

#tv0 = RootToken()
#tv0 + LinearToken("text", 1, "this is the first level ")
#tv0 + NestingToken("strong", 3, "**")
#tv0 + LinearToken("text", 3, " this is the second level ")
#tv0 + NestingToken("em", 5, "_")
#tv0 + LinearToken("text", 5, " this is the third level ")
#tv0 + NestingToken("em", 5, "_")
#tv0 + LinearToken("text", 3, " continueing the second level ")
#tv0 + LinearToken("code", 5, " this is a new third level ")
#tv0 + LinearToken("text", 3, " back to the second level ")
#tv0 + NestingToken("strong", 3, "**")
#tv0 + LinearToken("text", 1, " this is the end of the first level")
#
#print(tv0.nested)
#print("done")

# %%
