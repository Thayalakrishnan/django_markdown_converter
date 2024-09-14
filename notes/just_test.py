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

def ConvertListIntoItems(source:str=""):
    items = []
    
    lineitempattern = re.compile(r'(?:^\s*?- ).*?(?=^\s*?- )|(?:^\s*- ).*?$\n?', re.MULTILINE | re.DOTALL)
    line_id_pattern = re.compile(r'^(?P<level>\s*?)(?P<marker>- )(?P<first>.*?\n)(?P<rest>.*?$\n?)?', re.DOTALL)
    line_id_pattern = re.compile(r'^(?P<level>\s*?)(?P<marker>- )(?P<content>.*?$\n?)?', re.DOTALL)
    
    lines = lineitempattern.findall(source)

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
    return items

def CreateBlockFromItem(item:tuple=()):
    #level = len(item[0])
    #content = current_line["content"].strip().split("\n")
    #content = [_.lstrip() for _ in content]
    #current_line["content"] = "\n".join(content)
    return
    

# %%
def GroupLines(items):
    """
    """
    root = {"level": 0, "content": "root", "children": []}
    cur_parent = root
    cur_lvl = root["level"]
    
    stack = []
    stack_level = []
    
    index = 0
    max_index = len(items)
    item = next(items)
    while index < max_index:
        #item = items[index]
        
        if item["level"] < cur_lvl:
            cur_parent = stack.pop()
            cur_lvl = stack_level.pop()
        elif item["level"] > cur_lvl:
            """
            if the current items level is bigger than the 
            the current level, it is nested under the current item
            """
            stack.append(cur_parent)
            stack_level.append(cur_lvl)
            cur_lvl = item["level"]
            cur_parent = cur_parent["children"][-1]
        else:
            cur_parent["children"].append(item)
            index+=1
    return root["children"]
# %%



def ConvertListIntoItemsTwoStep(source:str=""):
    items = []
    lineitempattern = re.compile(r'(?:^\s*?- ).*?(?=^\s*?- )|(?:^\s*- ).*?$\n?', re.MULTILINE | re.DOTALL)
    line_id_pattern = re.compile(r'^(?P<level>\s*?)(?P<marker>- )(?P<content>.*?$\n?)?', re.DOTALL)
    
    lines = lineitempattern.findall(source)
    for line in lines:
        match = line_id_pattern.match(line)
        if match:
            current_line = match.groupdict()
            #current_line["level"] = len(current_line["level"])
            #content = current_line["content"].strip().split("\n")
            #content = [_.lstrip() for _ in content]
            #current_line["content"] = "\n".join(content)
            items.append(tuple(current_line.values()))
    return items

# %%


md = """- Item 1: line 1.
  Item 1: line 2.
- Item 2: line 1.
  Item 2: line 2.
  
  Item 2: line 3.
  - Item 2.1: line 1.
  - Item 2.2: line 1.
  - Item 2.3: line 1.
    1. Item 2.3.1: line 1.
    2. Item 2.3.2: line 1.
    3. Item 2.3.3: line 1.
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


dink
"""


md = """
- Item 1.
- Item 2.
    - Item 2.1.
    - Item 2.2.
    - Item 2.3.
        - Item 2.3.1
        - Item 2.3.2
        - Item 2.3.3
    - Item 2.4
    - Item 2.5
        - Item 2.5.1
        - Item 2.5.2
        - Item 2.5.3
    - Item 2.6
- Item 3.
"""

# %%
import re

def FormatItem(item:dict=()):
    item["type"] = "item"
    item["level"] = len(item["level"])
    item["marker"] = "ulist" if item["marker"] == "- " else "olist"
    item["children"] = None
    content = item["content"].strip().split("\n")
    content = [_.lstrip() for _ in content]
    item["content"] = "\n".join(content)
    return item


def ConvertListIntoItems(source:str=""):
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>- )(?P<content>(?:.*?(?=^\s*?- ))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d{1,3}\. ))(?P<content>(?:.*?(?=^\s*?- ))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<content>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    return lineitempattern.finditer(source)


def ConvertListIntoItemGenerator(source:str=""):
    items = ConvertListIntoItems(source)
    current_item = FormatItem(next(items).groupdict())
    next_item = None
    try:
        for item in items:
            next_item = FormatItem(item.groupdict())
            yield current_item
            current_item = next_item
    except StopIteration:
        current_item = next_item
        pass
    current_item = next_item
    yield current_item


def AddItemToList(parent, child):
    del child["marker"]
    del child["level"]
    parent.append(child)

def ConvertList(source):
    """
    """
    items = ConvertListIntoItems(source)
    
    root = {
        "level": -2, 
        "type": "root", 
        "props": {}, 
        "children": None
    }
    cur_parent = {"children": [root]}
    
    cur_lvl = -2
    
    stack = []
    stack_level = []
    
    for next_item in items:
        item = FormatItem(next_item.groupdict())
        
        while True:
        
            if item["level"] < cur_lvl:
                cur_parent, cur_lvl = stack.pop()
                #cur_lvl = stack_level.pop()
            elif item["level"] > cur_lvl:
                """
                if the current items level is bigger than the 
                the current level, it is nested under the current item
                """
                stack.append((cur_parent, cur_lvl))
                #stack_level.append(cur_lvl)
                
                cur_lvl = item["level"]
                cur_parent = cur_parent["children"][-1]
                #cur_parent = previous_item
                
                # if there are no current children, add a list
                if not cur_parent["children"]:
                    cur_parent["type"] = item["marker"]
                    cur_parent["children"] = []
            else:
                AddItemToList(cur_parent["children"], item)
                break
    del root["level"]
    return root


#method1 = ConvertListIntoItemsOneStep(md)
method2 = ConvertList(md)

print(method2)
print("Done!")

# %%
