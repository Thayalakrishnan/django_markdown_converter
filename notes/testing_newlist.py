#%%
import re
from textwrap import dedent


source = """- Item 1a
- Item 2a
  
  Item 2b
- Item 3a
- Item 4a
    - Item 4a.1a
      Item 4a.1b
      
      Item 4a.1c
        - Item 4a.1c.1a
        - Item 4a.1c.2a
        - Item 4a.1c.3a
    - Item 4a.2a
    - Item 4a.3a
      
      ```python
      for p in range(3):
          print(p)
      ```
      
      Item 4a.3b
    - Item 4a.4a
        - Item 4a.4a.1a
        - Item 4a.4a.2a
    - Item 4a.5a
- Item 5a

"""
#%%

pattern = re.compile(r"(?:^- )(?P<first>.*\n)(?P<rest>(?:^ .*?\n)*)", re.MULTILINE)
items = pattern.findall(source)

newitems = []

def remove_padding(source:str=""):
    padding_pattern = re.compile(r"^ {0,}", re.MULTILINE)
    m = padding_pattern.match(source)
    if m:
        padding = len(m.group(0))
    source = "\n".join([line.removeprefix(" "*padding) for line in source.splitlines()])
    return source

for first,rest in items:
    if rest:
        content = "".join([first, remove_padding(rest)])
    else:
        content = first.strip()
    newitems.append({"name": "item", "data": {"content": content}})
    

[print(_) for _ in newitems]



#%%

pattern = re.compile(r"(?:^- )(?P<first>.*\n)(?P<rest>(?:^ .*?\n)*)", re.MULTILINE)
pattern = re.compile(r"(?P<padding>^ *?)(?P<marker>- )(?P<item>.*?)(?=(?:^ *?- )|(?:^\n))", re.MULTILINE | re.DOTALL)
pattern = re.compile(r"(?P<padding>^ *?)(?:- )(?P<item>.*?)(?=(?:^ *?- )|(?:^\n))", re.MULTILINE | re.DOTALL)

newitems = []

def remove_padding(source:str="", padding:int=0):
    source = "\n".join([line.removeprefix(" "*padding) for line in source.splitlines()])
    return source


items = pattern.finditer(source)
for item in items:
    #print(item.groupdict())
    current_item = list(item.groups())
    padding = len(current_item[0])
    content = remove_padding(current_item[1], padding)
    current_item[0] = padding
    print(current_item)
    #print(repr(item.group("padding")))
    
#%%
PADDING = 4

pattern = re.compile(r"(?P<padding>^ *?)(?P<marker>- )(?P<first>.*\n)(?P<second>(?:^ .*?\n)*?)(?=(?:^ *?- )|(?:^\n))", re.MULTILINE)
pattern = re.compile(r"(?P<padding>^ *?)(?:- )(?P<first>.*\n)(?P<second>(?:^ .*?\n)*?)(?=(?:^ *?- )|(?:^\n))", re.MULTILINE)
newitems = []

"""
so the first line of each item will include the padding in general which we can 
"""

#items = (item.groups() for item in pattern.finditer(source))
for padding, first, second in (item.groups() for item in pattern.finditer(source)):
    print(first)
    newitems.append([len(padding), ])

# %%
"""
Item 4a.3a
      
      ```python
      for p in range(3):
          print(p)
      ```
      
      Item 4a.3b


Item 4a.3a\n      \n      ```python\n      for p in range(3):\n          print(p)\n      ```\n      \n      Item 4a.3b\n
"""
source = "Item 4.1.5\n    \n      ```python\n      for p in range(3):\n          print(p)\n      ```\n      \n      Item 4.1.6\n"
padding = 4
source = "\n".join([line.removeprefix(" "*padding) for line in source.splitlines()])


