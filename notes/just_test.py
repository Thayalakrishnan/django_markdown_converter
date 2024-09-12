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


def GroupLines(items:list=[]):
    stack = []
    root = [0, '', []]
    
    current_block = root
    current_block_arr = root[2]
    
    current_level = 0
    stack.append(root)
    
    for item in items:
        #print(f"current_level: {current_level} item: {item[1]}")
        if item[0] < current_level: 
            while item[0] < current_level:
                #print(f"current: {current_level} target: {item[0]}")
                #print(stack)
                current_block = stack.pop()
                current_level = current_block[0]
                current_block_arr = current_block[2]
                
            current_block = stack.pop()
            current_level = current_block[0]
            current_block_arr = current_block[2]
            current_block_arr.append(item)
        elif item[0] > current_level:
            # update level
            current_level = item[0]
            
            # push current level to stack
            stack.append(current_block)
            
            # reference new level, which is the previous level
            current_block = current_block_arr[-1]
            current_block_arr = current_block[2]
            
            # add current item as child of new level
            current_block_arr.append(item)
        else:
            current_block_arr.append(item)
    return root[2]

print(GroupLines(mylines))
# %%
