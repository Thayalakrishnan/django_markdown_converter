
# %%
import re
from typing import Generator

PATTERN_LI = re.compile(r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)')

PATTERN_INDENTATION = re.compile(r'^(?P<indentation>\s*)(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)')

# match the start of the line
# look for a dash to indicate list item
# look for a space aftter the dash
PATTERN_UL = re.compile(r'^(\s*)(-)(\s+)(.+?)(?=\n{2}|$)')

PATTERN_IS_LI = re.compile(r'^(\s*)(-)(\s+)(.+?)(?=\n{2}|$)')
PATTERN_UL = re.compile(r'^(-)(\s+)(.+?)(?=\n{2}|$)')
BANK = []

def extract_indentation_info(match):
    return (len(match.group('indentation')), match.group('content'))

def return_indentation_tuple(line):
    match = PATTERN_INDENTATION.match(line)
    return extract_indentation_info(match)

def test_ulist_item(line):
    return PATTERN_UL.match(line)
    
def get_line_type(line):
    return "ul"
    
def extract_line_info(match):
    return (match.group('indentation'), match.group('marker'), match.group('content'))

def yieldGroupedLines(lines) -> Generator[int, None, None]:
    """
    this function takes multi line list items and groups them together
    loops through the lines provided
    - if the new line is a list item, 
        - we yield the current line that is being held
        - we assign the new line to a new array and point to that array
    - if the line is not a list item we add it the current array
    """
    current_line_ptr = []
    for newline in lines:
        # test if this is the start of a new li
        if test_ulist_item(newline):
            # if the current line  is the start of a new line
            # we need to store the old line before we assign the nwe one 
            # to curren tline
            if current_line_ptr:
                yield current_line_ptr
                
            # set the current line to the new line
            current_line_ptr = [newline]
        else:
            #current_line_ptr.append(newline.lstrip())
            current_line_ptr.append(newline)
        
    yield current_line_ptr
    
def blockify(lines):
    result = []
    grouped_lines = yieldGroupedLines(lines)
    
    for lines in grouped_lines:
        #print(lines)
        main_line = lines[0]
        match = PATTERN_LI.match(main_line)
        
        if match:
            indentation, marker, content = extract_line_info(match)
            level = len(indentation)
            # loop through the children and find the smallest list level
            # loop through the children and find the smallest list level
            if len(lines) > 1:
                children = lines[1::]
            else:
                children = []
                
            for i in children:
                limatch = PATTERN_IS_LI.match(i)
                if limatch:
                    i = i.lstrip("  ")
                    print(f"list item : {i}")
            
            item = new_create_list_item(get_line_type(main_line), level, marker, content, children)
            result.append(item)
            
    #print(f"----------------------- flat list ----------------------------")                 
    #print(result)
    #return process_list_items(result)
    return result

    
def new_create_list_item(lineType:str, level:int, marker:str, content:str, children:list=[]) -> dict:
    return {
        "type": "li",
        "level": level,
        'children': children,
        "data": content
    }


# %%
md = [
    f'- UnOrdered List Item 1.',
    f' Multiline list item for list item 1.',
    f' Multiline list item for list item 2.',
    f' Multiline list item for list item 3.',
    f'- UnOrdered List Item 2',
    f' Multiline list item for list item 2.',
    f'    - UnOrdered List Item 2 Nested item 1',
    f'    - UnOrdered List Item 2 Nested item 2',
    f'- UnOrdered List Item 3',
]

for m in md:
    ret = return_indentation_tuple(m)
    print(ret)


#output = blockify(md)
#for b in output:
#    print(b)
#    #for c in b["children"]:
#    #    print(c)
#    #else:
#    #    print(b)
##glinese = yieldGroupedLines(md)
##for l in glinese:
##    print(l)
print("done")
# %%
