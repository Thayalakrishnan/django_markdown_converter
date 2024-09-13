#%%
import re

md = """- Item 1: line 1.
- Item 2: line 1.
- Item 3: line 1.
- Item 4: line 1."""

md = """- Item 1: line 1.
- Item 2: line 1.
- Item 3: line 1.
  - Item 3.1: line 1.
  - Item 3.2: line 1.
- Item 4: line 1."""



md = """- Item 1: line 1.
  Item 1: line 2.
- Item 2: line 1.
  Item 2: line 2.

  Item 2: line 3.
- Item 3: line 1.
  - Item 3.1: line 1.
    Item 3.1: line 2.

    ```python
    for p in range(3):
        print(p)
    ```

    Item 3.1: line 3.
  - Item 3.2: line 1.
- Item 4: line 1.
"""


"""
# this works real well
(?:^\s*?- ).*?(?=^\s*?- )|(?:^\s*- ).*?$
"""


items = []
#lines = md.split("\n")
lines = re.split(pattern=r"^ *?- ", string=md, flags=re.MULTILINE | re.DOTALL)
lines = re.split(pattern=r"^- ", string=md, flags=re.MULTILINE | re.DOTALL)

sublinepattern = re.compile(r'\n(?=^\S[^-])', re.MULTILINE | re.DOTALL)
lineitempattern = re.compile(r'(?:^\s*?- ).*?(?=^\s*?- )|(?:^\s*- ).*?$', re.MULTILINE | re.DOTALL)

for line in lines:
    if not line:
        continue

    multiline = line.count("\n") > 1
    nested = ""

    if multiline:
        sublines = [_.removeprefix("  ") for _ in line.split("\n")]
        line = "\n".join(sublines)
        line = re.sub(sublinepattern, '\n\n', line)
    else:
        line = line.strip("\n")

    items.append({
        "type": "item",
        "multiline": multiline,
        "data": line,
    })


for _ in items:
    #print("item ----------------------")
    print(repr(_["data"]))




# %%

md = """- Item 1: line 1.
  Item 1: line 2.
- Item 2: line 1.
  Item 2: line 2.

  Item 2: line 3.
  - Item 2.1: line 1.
  - Item 2.2: line 1.
  - Item 2.3: line 1.
    - Item 2.3.1: line 1.
    - Item 2.3.2: line 1.
    - Item 2.3.3: line 1.
  - Item 2.4: line 1.
- Item 3: line 1.
  - Item 3.1: line 1.
    Item 3.1: line 2.

    ```python
    for p in range(3):
        print(p)
    ```

    Item 3.1: line 3.
  - Item 3.2: line 1.
- Item 4: line 1.
"""

ref_stack = []
items = []
current_level = []

lineitempattern = re.compile(r'(?:^\s*?- ).*?(?=^\s*?- )|(?:^\s*- ).*?$\n?', re.MULTILINE | re.DOTALL)
line_id_pattern = re.compile(r'^(?P<level>\s*?)(?P<marker>- )(?P<first>.*?\n)(?P<rest>.*?$\n?)?', re.DOTALL)
line_id_pattern = re.compile(r'^(?P<level>\s*?)(?P<marker>- )(?P<content>.*?$\n?)?', re.DOTALL)

lines = lineitempattern.findall(md)

for line in lines:
    match = line_id_pattern.match(line)
    if match:
        newline = []
        current_line = match.groupdict()
        current_line["level"] = len(current_line["level"])
        content = current_line["content"].strip().split("\n")
        content = [_.lstrip() for _ in content]
        current_line["content"] = "\n".join(content)
        items.append(list(current_line.values()))

for _ in items:
    print(_)
    



# %%

mylines = [
    [0, 'Item 1', []],
    [0, 'Item 2', []],
    [2, 'Item 2.1', []],
    [2, 'Item 2.2', []],
    [2, 'Item 2.3', []],
    [4, 'Item 2.3.1', []],
    [4, 'Item 2.3.2', []],
    [4, 'Item 2.3.3', []],
    [0, 'Item 3', []],
    [2, 'Item 3.1', []],
    [2, 'Item 3.2', []],
    [0, 'Item 4', []],
]


mylines = [
    [0, 'Item 1', []],
    [2, 'Item 1.1', []],
    [4, 'Item 1.1.1', []],
    [6, 'Item 1.1.1.1', []],
    [8, 'Item 1.1.1.1.1', []],
    [6, 'Item 1.1.1.2', []],
    [4, 'Item 1.1.2', []],
    [6, 'Item 1.1.2.2', []],
    [4, 'Item 1.1.3', []],
]

mylines = [
    [0, 'Item 1', []],
    [2, 'Item 1.1', []],
    [4, 'Item 1.1.1', []],
    [6, 'Item 1.1.1.1', []],
    [8, 'Item 1.1.1.1.1', []],
]

mylines = [
    [0, 'Item 1', []],
    [0, 'Item 2', []],
    [0, 'Item 3', []],
    [0, 'Item 4', []],
    [0, 'Item 5', []],
]

# %%
mylines = [
    [0, 'Item 1', []],
    [0, 'Item 2', []],
    [2, 'Item 2.1', []],
    [4, 'Item 2.1.1', []],
    [0, 'Item 3', []],
    [0, 'Item 4', []],
    [2, 'Item 4.1', []],
    [4, 'Item 4.1.1', []],
    [0, 'Item 5', []],
]

def GroupLines(items:list=[]):
    stack = []
    root = [0, '', []]
    
    cur_parent = root
    cur_parent_arr = root[2]
    
    cur_lvl = 0
    stack.append(root)
    
    index = 0
    max_index = len(items)
    
    while index < max_index:
        item = items[index]
        #print(f"cur_lvl: {cur_lvl} item: {item[1]}")
        if item[0] < cur_lvl:
            #while item[0] < cur_lvl:
            #    #print(f"current: {cur_lvl} target: {item[0]}")
            #    #print(stack)
            #    cur_parent = stack.pop()
            #    cur_lvl = cur_parent[0]
            #    cur_parent_arr = cur_parent[2]
                
            cur_parent = stack.pop()
            cur_lvl = cur_parent[0]
            cur_parent_arr = cur_parent[2]
            #cur_parent_arr.append(item)
        elif item[0] > cur_lvl:
            """
            if the current items level is bigger than the 
            the current level, it is nested under the current item
            """
            # update level
            cur_lvl = item[0]
            
            # push current level to stack
            stack.append(cur_parent)
            
            # reference new level, which is the previous level
            cur_parent = cur_parent_arr[-1]
            cur_parent_arr = cur_parent[2]
            
            # add current item as child of new level
            #cur_parent_arr.append(item)
            #index+=1
        else:
            cur_parent_arr.append(item)
            index+=1
    return root[2]

print(GroupLines(mylines))
# %%
