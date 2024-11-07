#%%
import random
from faker import Faker

fake = Faker()

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)

SCAFFOLD_JOINLINES = lambda x=[]: "\n".join(x)

LAM_RANDOM_INT = lambda l,u: random.randint(l,u)
LAM_RANDOM_RANGE = lambda l,u: range(LAM_RANDOM_INT(l,u))

LAMGEN_FAKE_WORDS = lambda l=1,u=5: LAM_SPACED_JOIN(fake.words(nb=LAM_RANDOM_INT(l,u)))
LAMGEN_DECISION = lambda w=50: random.randint(1,100) < w

LAM_CLAMP = lambda l,u,x: max(min(x, u), l)
LAM_LIST_INDENT_UNDENT = lambda x: x + random.choice([-1, -1, 0, 0, 0, 1, 1])
LAM_ADJUST_LIST_INDENTATION = lambda x: LAM_CLAMP(0,6,LAM_LIST_INDENT_UNDENT(x))


def generate_list_item(list_type:str="u", level:int=0, counter:int=1):
    indent = level*' '*4
    delimter = "- " if list_type == "u" else f"{counter}. "
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return f"{indent}{delimter}{content}"

def generate_list_recursively(max_items:int=0, items:list=[], list_type:str="u", counter:int=1, indentation:int=1, count_stack:list=[]):
    if len(items) > max_items:
        return items
    
    new_item = generate_list_item(list_type, indentation, counter)
    items.append(new_item)
    new_indentation = LAM_ADJUST_LIST_INDENTATION(indentation)
    
    # indent
    if new_indentation > indentation:
        count_stack.append(counter)
        #indentation+=1
        #counter = 1
        generate_list_recursively(max_items, items, list_type, 1, indentation+1, count_stack)
    # unindent
    elif new_indentation < indentation:
        #counter = count_stack.pop()
        #counter +=1
        #indentation-=1
        generate_list_recursively(max_items, items, list_type, count_stack.pop() + 1, indentation-1, count_stack)
    else:
        counter +=1
        generate_list_recursively(max_items, items, list_type, counter, indentation, count_stack)
    
    #if len(items) > max_items:
    #    return items
    #return items

    #else:
    #    return generate_list_recursively(max_items, items, list_type, counter, indentation, count_stack)
        
def generate_list(list_type=""):
    items = []
    count_stack = []
    indentation = 0
    counter = 1
    max_items = random.randint(1,20)
    
    #while len(items) < max_items:
    #items, list_type, counter, indentation, count_stack = generate_list_recursively(max_items, items, list_type, counter, indentation, count_stack)
    generate_list_recursively(max_items, items, list_type, counter, indentation, count_stack)
    return SCAFFOLD_JOINLINES(items)


def generate_ulist():
    return generate_list("u")

def generate_olist():
    return generate_list("o")


def run_single_generator():
    for i in range(5):
        print(generate_olist())
        print("\n")

run_single_generator()

# %%
