from proto.person import Person
from proto.tokenizer import Tokenizer

def move_children_from_parent_to_grandparent(stack:list=[]) -> Person:
    #print(f"[proto][parser][move_children_from_parent_to_grandparent]")
    """
    move all the children from the current parent
    to the grandparent
    """
    current_parent = stack.pop()
    previous_child = current_parent.remove_last_child()
    current_parent.add_children(previous_child.children)
    return current_parent

def initialise_new_parent(stack:list=[], parent:Person=None, token:str="text"):
    """
    create a new parent and make the current parent 
    """
    #print(f"[proto][parser][initialise_new_parent]")
    new_parent = Person(token=token, parent=parent)
    parent.add_child(new_parent)
    stack.append(parent)
    return new_parent


def parse_inline_tokens(tokens):
    #print(f"[proto][parser][parse_inline_tokens]")
    object_stack = []
    root = Person("root", [])
    current_parent = root
    
    for token, value, nestable, isopen in tokens:
        if not nestable:
            if token == "text" and not len(value):
                continue
            new_child = Person(token, value, current_parent)
            current_parent.add_child(new_child)
        else:
            if isopen:
                # assign the new object as the current object
                current_parent = initialise_new_parent(object_stack, current_parent, token)
            else:
                # if the token is closed
                # when we close a formatting context, we need change parents
                if len(object_stack):
                    while token != current_parent.token:
                        current_parent = move_children_from_parent_to_grandparent(object_stack)
                    current_parent = object_stack.pop()
    
    # so if we still have depth that means we havent closed one of our boundaries
    while len(object_stack):
        move_children_from_parent_to_grandparent(object_stack)
        
    return root.get_representation()


def parse(source:str="")-> list:
    #print(f"[proto][parser][parse]")
    tokens = Tokenizer.tokenize(source)
    ret = parse_inline_tokens(tokens)
    return ret[1]
    