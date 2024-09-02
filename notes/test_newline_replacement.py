import re

def print_lines(content):
    lines = content.split("\n")
    for i in lines:
        print(repr(i))
    return "\n".join(lines)

def process_input_content(content:str="")-> str:
    # create and compile pattern
    NEWLINE_REPLACE_RAW = r'^\n{2,}'
    NEWLINE_REPLACE_PATTERN = re.compile(NEWLINE_REPLACE_RAW, re.MULTILINE | re.DOTALL)
    
    # replace the newlines
    processed_content = content.strip("\n ")
    processed_content = re.sub(NEWLINE_REPLACE_PATTERN, "\n", processed_content)
    
    # add new lines at the end for matcing purposes
    processed_content = processed_content + "\n\n"
    return processed_content

def space_replace_content(content:str="")-> str:
    SPACE_REPLACE = r'(?:.{1})\s(?:.{1})'
    SPACE_REPLACE = r'(?=.)\s(?=.)'
    SPACE_REPLACE_PATTERN = re.compile(SPACE_REPLACE, re.MULTILINE)
    processed_content = re.sub(SPACE_REPLACE_PATTERN, "•", content)
    return processed_content

raw_content = """
## heading



This is come content.

This is some other content. 

## This is anothe heading

This is the third sentence. 


"""

print("before -----------------------------")
print_lines(raw_content)

print("after ------------------------------")
raw_content = process_input_content(raw_content)
print_lines(raw_content)

print("after ------------------------------")
raw_content = space_replace_content(raw_content)
print_lines(raw_content)

print("done -------------------------------")
