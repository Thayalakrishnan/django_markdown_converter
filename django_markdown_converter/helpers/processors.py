import re


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



def extract_attrs(content:str="")-> str:
    # attrs
    attrs = ""
    EXTRACT_ATTRS = r'(?P<before>.*)\{(?P<attrs>.*?)\}(?P<after>.*)'
    ATTRS_PATTERN = re.compile(EXTRACT_ATTRS, re.MULTILINE | re.DOTALL)
    
    match = ATTRS_PATTERN.match(content)
    if match:
        ## if there are attrs, extract them
        attrs = match.group("attrs")
        ## return the content without the attrs
        content = match.group("before") + match.group("after")
    return content, attrs