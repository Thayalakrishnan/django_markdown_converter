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

## multiline before starting a nested list
md = """- Item 1: line 1.
- Item 2: line 1.
  Item 2: line 2.
  Item 2: line 3.
  - Item 2.1: line 1.
  - Item 2.2: line 1.
    Item 2.2: line 2.
    Item 2.2: line 3.
  - Item 2.3: line 1.
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

md = """
- Item 1 line 1.
  Item 1 line 2.
  
  Item 1 line 3.
- Item 2 line 1.
- Item 3 line 1.
"""


#%%


md = """- Item 1: line 1.
- Item 2: line 1.
  - Item 2.1: line 1.
  - Item 2.2: line 1.
    - Item 2.2.1: line 1.
    - Item 2.2.2: line 1.
- Item 3: line 1.
"""

# %%
import re

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
        "data": [{"type": "text", "data": data}],
    }


def CreateListBlock(marker):
  return {
      "type": marker,
      "data": [],
  }


def ConvertListIntoItems(source:str=""):
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<data>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    return lineitempattern.finditer(source)

def AddItemToList(parent, child):
    del child["marker"]
    del child["level"]
    parent.append(child)


def ConvertList(source, bank):
    """
    """
    items = ConvertListIntoItems(source)
    stack = []
    root = {
        "level": 0,
        "type": "root",
        "data": []
    }
    
    cur_parent = root
    cur_lvl = 0

    for item in items:
        current_item = FormatItem(item.groupdict())
        bank.append(current_item)

        while True:
            if current_item["level"] < cur_lvl:
                cur_parent, cur_lvl = stack.pop()
            elif current_item["level"] > cur_lvl:
                """
                if the current items level is bigger than the
                the current level, it is nested under the current item
                """
                stack.append((cur_parent, cur_lvl))
                
                #cur_parent = cur_parent["data"][-1]
                cur_lvl = current_item["level"]
                if cur_parent["data"]:
                  previous_item = cur_parent["data"][-1]
                else:
                  previous_item = bank[-1]
                
                # create new list block using the current item
                newlistblock = CreateListBlock(current_item["marker"])
                #current_item["data"].append(newlistblock)
                #cur_parent = item["data"]
                previous_item["data"].append(newlistblock)
                cur_parent = newlistblock
                ## if there are no current children, add a list
                #if not cur_parent["children"]:
                #    cur_parent["type"] = current_item["marker"]
                #    cur_parent["children"] = []
            else:
                cur_parent["data"].append(current_item)
                #AddItemToList(cur_parent["children"], current_item)
                break
    del root["level"]
    
    for _ in bank:
      if "marker" in _:
        del _["marker"]
      if "level" in _:
        del _["level"]
      #if "children" in _ and not _["children"]:
      #    del _["children"]
    return root
mybank = []
ret = ConvertList(md, mybank)

print(ret)

#for _ in mybank:
#    print(_)
    
print("Done!")

# %%
