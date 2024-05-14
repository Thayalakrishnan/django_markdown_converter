# %%
import re

raw_chunk = [
    #'| Row 1 Column 1| Row 1 Column 2 |',
    #'| Row 3 Column 1| Row 2 Column 2 |',
    '| Column 1 Title | Column 2 Title |',
    '| ----------- | ----------- |',
    '| Row 1 Column 1| Row 1 Column 2 |',
    '| Row 2 Column 1| Row 2 Column 2 |',
    '{ id="small-table" caption="small table of values" }',
]
chunk = "\n".join(raw_chunk)
raw_pat = r'^(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n|\|$))+)(?:(?:\{\s*(?P<attrs>.*?)\s*\})?)' # this works

pattern = re.compile(raw_pat, re.MULTILINE | re.DOTALL)
match = pattern.search(chunk)

#$print("header")
#$print(match.group('header'))
#$#
#$print("settings")
#$print(match.group('settings'))
#$#
#$print("content")
#$print(match.group('content'))

content_chunk = match.group('content')
lines = content_chunk.split("\n")
print(lines)
#content = [[_.strip() for _ in line[1:-1].strip().split("|") if len(_) > 0] for line in lines]
content = [[_.strip() for _ in line[1:-1].strip().split("|") if len(_) > 0] for line in lines if len(line)]

print(content)
#if match.group('attrs'):
#    print("attrs")
#    print(match.group('attrs'))
    
print("done")

# %%
