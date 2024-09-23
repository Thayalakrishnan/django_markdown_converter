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
    this is a multiline item
    which leads into a nested list 
    - Item 2.2.1: line 1.
    - Item 2.2.2: line 1.
- Item 3: line 1.
"""

md = """- Item 1: line 1.
- Item 2: line 1.
    - Item 2.1: line 1.
        - Item 2.1.1: line 1.
    - Item 2.2: line 1.
- Item 3: line 1.
    - Item 3.1: line 1.
        - Item 3.1.1: line 1.
    - Item 3.2: line 1.
- Item 4: line 1.
"""

# %%
import re

def DetermineListType(marker):
    return "ulist" if marker == "- " else "olist"

def CreateListItem(yeet:dict=()):
    """
    TODO: use the level to set the amount of padding to remove
    from each line. it should be level + 1 i think, depending on
    type of list maybe
    """
    marker = yeet["marker"]
    level = len(yeet["level"])
    padding = level + len(marker)
    # the triple curly braces translates f'^ {{{padding}}}' --> f'^ {4}' for padding = 4
    data = re.sub(pattern=f'^ {{{padding}}}', repl='', string=yeet["data"], flags=re.MULTILINE)
    return {
        "type": "item",
        "level": level,
        "marker": DetermineListType(marker),
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
    
def FormatList(lst):
    for _ in lst:
      if "marker" in _:
        del _["marker"]
      if "level" in _:
        del _["level"]

def ConvertList(source, bank):
    """
    the way nested lists are rendered is by nesting them 
    under an item of the parent list
    our lists are mainly made up of items, lists and text blocks.
    (they are also comprised of other nested block elements)
    
    - to convert our lists, we need to iterate over the items and determine 
    the level of the item
    - if the current item has a larger level then the previous item,
    the current item should be nested under the previous item
    - so we create a new list block based of the current item
    - we then need to grab the previous item and place the new list block
    as as a child under the previous item
    """
    items = ConvertListIntoItems(source)
    stack = []
    root = {
        "level": -2,
        "type": "root",
        "data": []
    }
    
    cur_parent = {"data": [root]}
    cur_lvl = -2

    for item in items:
        current_item = CreateListItem(item.groupdict())
        bank.append(current_item)

        while True:
            if current_item["level"] < cur_lvl:
                cur_parent, cur_lvl = stack.pop()
            elif current_item["level"] > cur_lvl:
                """
                if the current items level is bigger than the
                the current level, it is nested under the current item
                
                the stack holds the reference to the parent items
                note: parent items will only ever reference an item that 
                can hold nested list items
                """
                # add the current level and the current parent to the stack
                stack.append((cur_parent, cur_lvl))
                
                # create new list block using the current item
                newlistblock = CreateListBlock(current_item["marker"])
                
                # our new parent needs to be the child of the previous item
                previous_item = cur_parent["data"][-1]
                
                # add the new list block as a child of the previous item
                previous_item["data"].append(newlistblock)
                
                # make the new list block the parent
                cur_parent = newlistblock
                
                # our new list level is created from the the current item
                cur_lvl = current_item["level"]
            else:
                cur_parent["data"].append(current_item)
                break
    
    ## format our final output using the bank
    FormatList(bank)
    return root["data"][0]

mybank = []
ret = ConvertList(md, mybank)

print(ret)

#for _ in mybank:
#    print(_)
    
print("Done!")

# %%
