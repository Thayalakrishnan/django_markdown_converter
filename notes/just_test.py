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

md = """
- Item 1.
"""

md = """- Item 1: line 1.
- Item 3: line 1.
  - Item 3.1: line 1.
    Item 3.1: line 2.
    
    ```python
    for p in range(3):
        print(p)
    ```
    
    Item 3.1: line 3.
  - Item 3.2: line 1.
    - Item 3.2.1: line 1.
    - Item 3.2.2: line 1.
      Item 3.2.2: line 2.
      
      ```python
      for p in range(3):
          print(p)
      ```
      
      Item 3.2.2: line 3.
- Item 4: line 1.
"""


# %%
import re
from textwrap import dedent

def FormatContent(fresh:str="", amount:int=1) -> str:
    fresh = fresh.strip().split("\n")
    for _ in fresh:
      print(repr(_))
    fresh = [_.strip(" ", amount) for _ in fresh]
    for _ in fresh:
      print(repr(_))
    return "\n".join(fresh)

def FormatItem(yeet:dict=()):
    """
    TODO: use the level to set the amount of padding to remove 
    from each line. it should be level + 1 i think, depending on 
    type of list maybe
    """
    
    level = len(yeet["level"])
    padding = level + len(yeet["marker"]) 
    
    data = yeet["data"]
    data = re.sub(pattern=f'^ {{{padding}}}', repl='', string=data, flags=re.MULTILINE) 
    
    return {
        "type": "item",
        "level": level,
        "marker": "ulist" if yeet["marker"] == "- " else "olist",
        "children": None,
        "data": data,
    }


def ConvertListIntoItems(source:str=""):
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<data>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    return lineitempattern.finditer(source)

def AddItemToList(parent, child):
    del child["marker"]
    del child["level"]
    parent.append(child)


def ConvertList(source):
    """
    """
    items = ConvertListIntoItems(source)
    stack = []
    bank = []
    
    root = {
        "level": -2, 
        "type": "root", 
        "props": {}, 
        "children": None
    }
    cur_parent = {"children": [root]}
    cur_lvl = -2
    
    for next_item in items:
        item = FormatItem(next_item.groupdict())
        bank.append(item)
        
        while True:
        
            if item["level"] < cur_lvl:
                cur_parent, cur_lvl = stack.pop()
            elif item["level"] > cur_lvl:
                """
                if the current items level is bigger than the 
                the current level, it is nested under the current item
                """
                stack.append((cur_parent, cur_lvl))
                cur_lvl = item["level"]
                cur_parent = cur_parent["children"][-1]
                
                # if there are no current children, add a list
                if not cur_parent["children"]:
                    cur_parent["type"] = item["marker"]
                    cur_parent["children"] = []
            else:
                AddItemToList(cur_parent["children"], item)
                break
    del root["level"]
    return root, bank


method2, b = ConvertList(md)

print(method2)

for _ in b:
    print(_)
print("Done!")

# %%
