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
LAM_LIST_INDENT_UNDENT = lambda x: x + random.choice([-1, 0, 1])
LAM_ADJUST_LIST_INDENTATION = lambda x: LAM_CLAMP(0,6,LAM_LIST_INDENT_UNDENT(x))


def generate_list_item(list_type:str="u", ctr:int=1, ind:int=0):
    indent = ind*' '*4
    delimter = "- " if list_type == "u" else f"{ctr}. "
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return f"{indent}{delimter}{content}"



#def generate_list_recursively(max_items:int=0, items:list=[], list_type:str="u", ctr:int=1, ind:int=1, stack:list=[]):
#    """
#    max, items, type, ctr, ind, 
#    stack: type, ctr, ind
#    """
#    if len(items) > max_items:
#        return items
#    
#    items.append(generate_list_item(list_type, ind, ctr))
#    new_ind = LAM_ADJUST_LIST_INDENTATION(ind)
#    
#    # indent
#    if new_ind > ind:
#        stack.append(ctr)
#        generate_list_recursively(max_items, items, list_type, 1, ind+1, stack)
#    # unindent
#    elif new_ind < ind:
#        generate_list_recursively(max_items, items, list_type, stack.pop() + 1, ind-1, stack)
#    # stay the same
#    else:
#        ctr +=1
#        generate_list_recursively(max_items, items, list_type, ctr, ind, stack)
#
#def generate_list(list_type=""):
#    items = []
#    max_items = random.randint(1,20)
#    generate_list_recursively(max_items, items, list_type, 1, 0, [])
#    return SCAFFOLD_JOINLINES(items)
#


def generate_list_recursively(max_items:int=0, items:list=[], current:list=[], stack:list=[]):
    """stack: type, ctr, ind"""
    if len(items) > max_items:
        return items
    
    list_type, ctr, ind = current
    items.append(generate_list_item(*current))
    new_ind = LAM_ADJUST_LIST_INDENTATION(ind)
    
    # indent
    if new_ind > ind:
        stack.append(current)
        current = [list_type, 1, ind+1]
    # unindent
    elif new_ind < ind:
        current = stack.pop()
        current[1] += 1
    # stay the same
    else:
        current = [list_type, ctr + 1, ind]
    generate_list_recursively(max_items, items, current, stack)

def generate_list(list_type=""):
    items = []
    max_items = random.randint(1,20)
    generate_list_recursively(max_items, items, [list_type, 1, 0], [])
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
