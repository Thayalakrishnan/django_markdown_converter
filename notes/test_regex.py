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
# %%
import re

raw_chunk = [
    '***  ',
    '',
]

chunk = "\n".join(raw_chunk)
#raw_pat = r'\n\*\*\*\n'
raw_pat = r'^(?P<content>\*\*\*)\s*\n'
raw_pat = r'^\s*(?P<content>\*\*\*)\s*(?:\n|$)'
pattern = re.compile(raw_pat, re.MULTILINE | re.DOTALL)
match = pattern.search(chunk)

if match.group('content'):
    content_chunk = match.group('content')
    print(content_chunk)
    
print("done")
# %%
# %%
import re

lines = [
    'This is the first sentence!',
    '',
    'This is the second sentence!',
    '',
]


# receive lines 
# create chunk 
# match chunk 
# if match, find end of match  
# return lines 
chunk = "\n".join(lines)
#raw_pat = r'(?P<content>(?:.*(?:\n|$)))'
raw_pat = r'(?P<content>.*?)(?:\n|$)'
pattern = re.compile(raw_pat, re.MULTILINE | re.DOTALL)

match = pattern.match(chunk)

if match.group('content'):
    # extract the start and end of the match
    #start = match.start()
    end = match.end()
    
    # the before chunk is everything up until the 
    # end index minus one
    before = chunk[:end-1]
    
    # the before chunk should be equal to the 
    # matched content
    before = match.group('content')
    
    # the after chunk
    after_chunk = chunk[end::]
    after_lines = after_chunk.split("\n")
    
    # once we process this block, the after_lines 
    # becomes the new lines 
    # the after chunk becomes the new chunk
    #assert match.group('content') == before
    print(f'before: {repr(before)}')
    print(f'after: {repr(after_chunk)}')
    print(lines)
    print(after_lines)
    
    
    
print("done")
# %%

# %%
import re

def extract_chunk(lines, pat):
    
    chunk = "\n".join(lines)
    match = pat.match(chunk)

    if match.group('content'):
        end = match.end()
        before = chunk[:end-1]
        before = match.group('content')
        after_chunk = chunk[end::]
        lines = after_chunk.split("\n")
        return lines
    else:
        return lines[1:]
    

og_lines = [
    'This is the first sentence!',
    '',
    'This is the second sentence!',
    '',
]

raw_pat = r'(?P<content>.*?)(?:\n|$)'
pattern = re.compile(raw_pat, re.MULTILINE | re.DOTALL)

num_lines = len(og_lines)
while num_lines:
    print(og_lines)
    og_lines = extract_chunk(og_lines, pattern)
    num_lines = len(og_lines)
    
print("done")
# %%
test_lines = [
    'This is the first sentence!',
    '',
    'This is the second sentence!',
    '',
]

for (index_start, line) in enumerate(test_lines):
    if not len(line):
        continue
    print(index_start)
    print(line)
    
print("done")
# %%
import re

test_lines = [
    '- List item 1',
    '- List item 2',
    '    - Indented List 2 Item 1',
    '    - Indented List 2 Item 2',
    '        - Indented List 2 Item 2 Item 1',
    '        - Indented List 2 Item 2 Item 2',
    '        - Indented List 2 Item 2 Item 3',
    '    - Indented List 2 Item 3',
    '',
    '',
    '- List item 3',
    '    - Indented List 3 Item 1',
    '    - Indented List 3 Item 2',
    '',
]

raw_pat = r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)'
raw_pat = r'^(?P<content>(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)'

# this works real well except for breakages in the list 
raw_pat = r'^(?P<content>(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<item>.+?)(?=\n{1}|$))+(?:\n|$)'

raw_pat = r'^(?P<content>(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<item>.+?)(?:\n|$))(?:\n|$)'

chunk = "\n".join(test_lines)

pattern = re.compile(raw_pat, re.MULTILINE | re.DOTALL)

match = pattern.match(chunk)
print("size:" + str(len(chunk)))

if match.group('content'):
    content = match.group('content')
    print(f"groups")
    print(match.groups())
    
    print(f"start: {match.start()}")
    print(f"end: {match.end()}")
    
    print(content)
    print(f"indentation: {match.group('indentation')}")
    print(f"marker: {match.group('marker')}")
    print(f"item: {match.group('item')}")

#matches = pattern.findall(chunk)
#print(type(matches))
#if matches:
#    for m in matches:
#        print(dir(m))
        
matches = pattern.finditer(chunk)
print(type(matches))
if matches:
    for m in matches:
        #print(m.start())
        print(len(m.group("indentation")))
        print(m.group("item"))
        #print(type(m))

# %%
