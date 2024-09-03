import re

META_BLOCK_PATTERN = r'^(?:---\n)(?P<content>.*?)(?:---\n)'

META_BLOCK_PATTERN = r'(?:^---.*?$)(?P<content>.*?)(?:^---.*?$)'
META_BLOCK_PATTERN = r'^---.*?$.*?^---.*?$'
META_BLOCK_DATA = re.compile(META_BLOCK_PATTERN, re.MULTILINE | re.DOTALL)

raw_chunk = """---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---
"""

match = META_BLOCK_DATA.match(raw_chunk)

if match:
    print("Match -------------------")
    print(match)
    #print(match.group("content"))

