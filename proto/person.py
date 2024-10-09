class Person:
    __slots__ = ['token', 'children', 'parent', ]
    
    def __init__(self, token:str="", children:list=[], parent=None):
        self.token = token
        self.children = []
        self.parent = parent
        
        if children:
            self.children = children
            
    @property
    def first_child(self):
        return self.children[0]
    
    @property
    def last_child(self):
        return self.children[-1]
    
    @property
    def has_single_child(self):
        return len(self.children) == 1
    
    @property
    def has_children(self):
        return isinstance(self.children, list) and len(self.children)
    
    @property
    def has_content(self):
        return isinstance(self.children, str)
    
    def add_child(self, child):
        child.parent = self
        if self.has_children:
            # merge kids if they are the same token
            if self.last_child.token == child.token and self.last_child.has_content and child.has_content:
                self.last_child.children = self.last_child.children + child.children
                del child
                return
        self.children.append(child)
                
    def add_children(self, children:list=[]):
        for child in children:
            self.add_child(child)
        
    def remove_last_child(self):
        return self.children.pop()

    def get_representation(self):
        """
        get the representation of the parent
        """
        # if the children is a list
        if self.has_children:
            # if there is only only child
            if self.has_single_child:
                if self.first_child.token == "text":
                    return [self.token, self.first_child.children]
                return [self.token, self.first_child.get_representation()]
            else:
                return [self.token, [_.get_representation() for _ in self.children]]
        # if the children is a string
        elif self.has_content:
            return [self.token, self.children]
        # if we are not sure
        else:
            return [self.token, self.children.get_representation()]    
