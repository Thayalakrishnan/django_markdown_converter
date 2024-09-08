# %%
import re
from pathlib import Path
import os

    
md = """---
title:  Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---
"""

kvs_dict = {}

META_PATTERN_RAW = r'^---(?P<data>.*?)\n^---'
META_PATTERN = re.compile(META_PATTERN_RAW, re.MULTILINE | re.DOTALL)

KVP_PATTERN_RAW = r'^(?P<key>.*?)(?:\:\s*)(?P<value>.*?)(?:\n|$)'
KVP_PATTERN = re.compile(KVP_PATTERN_RAW, re.MULTILINE | re.DOTALL)

match = META_PATTERN.match(md)

if match:
    data = match.group("data").strip()
    print(data)
    
    if data:
        kvps = KVP_PATTERN.findall(data)
        print(kvps)

    #    lines = data.split("\n")
    #    if lines:
    #        kvs = [tuple(map(lambda x: x.strip(), line.split(":"))) for line in lines]
    #        if kvs:
    #            kvs_dict.update(dict(kvs))

#print(kvs_dict)
# %%
