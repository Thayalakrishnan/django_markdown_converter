#%%
import re
from textwrap import dedent


source = """- Item 1.1
- Item 2.1
  
  Item 2.2
- Item 3.1
- Item 4.1
    - Item 4.1.1
      Item 4.1.2
      
      Item 4.1.3
        - Item 4.1.3.1
          Item 4.1.3.2
          
          Item 4.1.3.3
    - Item 4.1.4
    - Item 4.1.5
      
      ```python
      for p in range(3):
          print(p)
      ```
      
      Item 4.1.6
    - Item 4.1.7
        - Item 4.1.7.1
    - Item 4.1.8
- Item 5.1

"""

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

# %%
