#%%
import random
from faker import Faker

fake = Faker()

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)
SCAFFOLD_JOINLINES = lambda x=[]: "\n".join(x)

LAM_RANDOM_INT = lambda l,u: random.randint(l,u)
LAMGEN_FAKE_WORDS = lambda l=1,u=5: LAM_SPACED_JOIN(fake.words(nb=LAM_RANDOM_INT(l,u)))

LAM_CLAMP = lambda l,u,x: max(min(x, u), l)
LAM_LIST_INDENT_UNDENT = lambda x: x + random.choice([-1, 0, 1])
LAM_ADJUST_LIST_INDENTATION = lambda x: LAM_CLAMP(0,6,LAM_LIST_INDENT_UNDENT(x))


def generate_list_item(list_type:str="u", ctr:int=1, ind:int=0):
    indent = ind*' '*4
    delimter = "- " if list_type == "u" else f"{ctr}. "
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return f"{indent}{delimter}{content}"

def generate_list_loop(items:list=[], current:list=[], stack:list=[]):
    """stack: type, ctr, ind"""
    items.append(generate_list_item(*current))
    new_ind = LAM_ADJUST_LIST_INDENTATION(current[2])
    current[1] += 1
    
    # indent
    if new_ind > current[2]:
        stack.append(current)
        return items, [current[0], 1, current[2]+1], stack
    # unindent
    elif new_ind < current[2]:
        return items, stack.pop(), stack
    # stay the same
    return items, current, stack


def generate_list(list_type=""):
    items, stack, current  = [], [], [list_type, 1, 0]
    max_items = random.randint(1,20)
    
    while len(items) < max_items:
        items, current, stack = generate_list_loop(items, current, stack)
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
