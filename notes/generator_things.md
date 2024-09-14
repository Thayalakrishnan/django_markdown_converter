```python
# %%

def LookAheadGenerator(items):
    current_item = next(items)
    try:
        for next_item in items:
            yield current_item
            current_item = next_item
    except StopIteration:
        pass
    yield current_item
    
    
mylist = [
    "item 1",
    "item 2",
    "item 3",
    "item 4",
    "item 5",
    "item 6",
]

mygen = (_ for _ in mylist)

#agen = LookAheadGenerator(mygen)

#for a in agen:
#    print(a)

for a in mygen:
    print(a)

# %%


import re

raw_pattern = r"yeet"
lineitempattern = re.compile(raw_pattern, re.MULTILINE | re.DOTALL)

md = """
my first yeet 
went a little like yeet 
and yeet
"""

mgen = lineitempattern.finditer(md)

for _ in mgen:
    print(_)



```