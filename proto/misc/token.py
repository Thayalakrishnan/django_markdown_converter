class TokenValue:
    __slots__ = ['name', 'value', ]
    
    def __init__(self, name:str="", value:list=[],):
        self.name = name
        self.value = value
    
    def __eq__(self, other):
        return self.name == other.name and type(self.value) == type(other.value) 
                    
    def __add__(self, other):
        if self == other:
            self.value = self.value + other.value
            del other
         
tv1 = TokenValue("yeet", "this is the start ")
tv2 = TokenValue("yeet", ", this is the end")

tv1 + tv2
print(tv1.value)
            