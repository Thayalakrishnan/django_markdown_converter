# %%
import re
    
md = """## this is a heading
 
 
this is a pargraph of content. this is a pargraph of content. this is a pargraph of content.
this is a pargraph of content. this is a pargraph of content. this is a pargraph of content.


## this is another heading 

- list item 1, sentence 1. 
   
  list item 1, sentence 2.
- list item 2
- list item 3


this is a second pargraph of content. this is a pargraph of content. this is a pargraph of content. 
this is a second pargraph of content. this is a pargraph of content. this is a pargraph of content. 

################################################################################
"""
# %%
#print(repr(md))
print(md)

# create and compile pattern
NEWLINE_REPLACE_RAW = r'^\n{2,}'
NEWLINE_REPLACE_PATTERN = re.compile(NEWLINE_REPLACE_RAW, re.MULTILINE | re.DOTALL)


# replace the newlines
processed_content = md.strip("\n ")
processed_content = re.sub(NEWLINE_REPLACE_PATTERN, "💩\n", processed_content)

# add new lines at the end for matcing purposes
processed_content = processed_content + "\n\n"

#print(repr(processed_content))
print(processed_content)
# %%
PATTERN_RAW = r'^.*?$'
PATTERN_RAW = r'^' # match start of every line
PATTERN_RAW = r'$' # match end of every line
PATTERN_RAW = r'\s$(?<!^)' # match whitespace at end of line
PATTERN_RAW = r' $(?<!^\s)'
PATTERN_RAW = r' $(?<!^)'
PATTERN_RAW = r'(?!^ +?\n) $'
PATTERN_RAW = r'(?!^😃+?\n)😃$'
PATTERN_RAW = r'(?<!^ )(?: $)'

PATTERN = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)

# replace the newlines
#processed_content = md.strip("\n ")
processed_content = re.sub(PATTERN, "💩", md)

# add new lines at the end for matcing purposes
processed_content = processed_content + "\n\n"

#print(repr(processed_content))
print(processed_content)
# %%
