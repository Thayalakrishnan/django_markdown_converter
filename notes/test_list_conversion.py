
# %%
import re
from typing import Generator

PATTERN_LI = re.compile(r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)')
PATTERN_INDENTATION = re.compile(r'^(?P<indentation>\s*)(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)')

# match the start of the line
# look for a dash to indicate list item
# look for a space aftter the dash
PATTERN_UL = re.compile(r'^(\s*)(-)(\s+)(.+?)(?=\n{2}|$)')
PATTERN_IS_LINE_ITEM = re.compile(r'^(\s*)(-)(\s+)(.+?)(?=\n{2}|$)')
PATTERN_UL = re.compile(r'^(-)(\s+)(.+?)(?=\n{2}|$)')
BANK = []

# %%
def extract_indentation_info(match):
    return (len(match.group('indentation')), match.group('content'))

def return_indentation_tuple(line):
    match = PATTERN_INDENTATION.match(line)
    return extract_indentation_info(match)


def test_if_line_item(line):
    return PATTERN_IS_LINE_ITEM.match(line)


def test_ulist_item(line):
    return PATTERN_UL.match(line)

def get_line_type(line):
    return "ul"

def extract_line_info(match):
    return (len(match.group('indentation')), match.group('marker'), match.group('content'))

def return_line_info(line):
    match = PATTERN_LI.match(line)
    return extract_line_info(match)

def return_line_content(line):
    return return_line_info(line)[2]

def process_line(line):
    
    match = PATTERN_LI.match(line)
    return extract_line_info(match)

# %%
def yieldGroupedLines(lines) -> Generator[int, None, None]:
    """
    this function takes multi line list items and groups them together
    loops through the lines provided
    - if the new line is a list item, 
        - we yield the current line that is being held
        - we assign the new line to a new array and point to that array
    - if the line is not a list item we add it the current array
    """
    current_group = []
    for newline in lines:
        
        if not len(newline):
            continue
        
        #level , current_line= return_indentation_tuple(newline)
        # test if this is the start of a new li
        if test_ulist_item(newline):
            
            # if the current line  is the start of a new line
            # we need to store the old line before we assign the nwe one to curren tline
            if current_group:
                yield current_group
            
            # set the current line to the new line
            
            current_group = [return_line_content(newline)]
        else:
            #current_group.append(newline.lstrip())
            if test_if_line_item(newline):
                current_group.append(newline.lstrip("    "))
            else:
                current_group.append(newline.lstrip())
        
    yield current_group

# %%
    
def blockify(lines):
    result = []
    grouped_lines = yieldGroupedLines(lines)
    
    for lines in grouped_lines:
        #print(lines)
        main_line = lines[0][2]
        match = PATTERN_LI.match(main_line)
        
        if match:
            level, marker, content = extract_line_info(match)
            
            # loop through the children and find the smallest list level
            if len(lines) > 1:
                children = lines[1::]
            else:
                children = []
            
            item = new_create_list_item(get_line_type(main_line), level, marker, content, children)
            result.append(item)
            
    return result

# %%

def new_blockify(lines):
    result = []
    grouped_lines = yieldGroupedLines(lines)
    
    for lines in grouped_lines:
        """
        - loop over the lines
        - each list item could potentially have a nested list in it
        - so we loop through the lines and determine what line group they all belong too 
        - we then need to handle the nesting
            - for each group of lines, we need to loop over the lines and determine the smallest padding
            - if a certain line does not have 
            - after removing the padding we determine if the 
        
        """
        #print(lines)
        #content = lines[0]
        
        # loop through the children and find the smallest list level
        if len(lines) > 1:
            children = lines
            content = ""
        else:
            children = []
            content = lines[0]
        
        item = new_create_list_item(get_line_type(content), content, children)
        result.append(item)
            
    return result


# %%

def new_create_list_item(
        lineType:str, 
        data:str, 
        children:list=[]
    ) -> dict:
    return {
        "type": "li",
        'children': children,
        "data": data
    }



# %%
md_raw = """
- UnOrdered List Item 1.
  Multiline list item for list item 1.
  Multiline list item for list item 2.
  Multiline list item for list item 3.
- UnOrdered List Item 2
  Multiline list item for list item 2.
    - UnOrdered List Item 2 Nested item 1
    - UnOrdered List Item 2 Nested item 2
- UnOrdered List Item 3
"""


md = md_raw.split("\n")[1::]

#for m in md:
#    ret = return_indentation_tuple(m)
#    print(ret)


output = new_blockify(md)
for b in output:
    print(b)
    #for c in b["children"]:
    #    print(c)
    #else:
    #    print(b)


#glinese = yieldGroupedLines(md)
#for l in glinese:
#    print(l)

print("done")
# %%
