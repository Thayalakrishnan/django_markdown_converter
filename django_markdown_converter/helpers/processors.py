import re


def process_input_content(content:str="")-> str:
    """
    transform the content by replacing multiple newline characters
    with a single newline character. 
    essentially we wan to ensure that the content is spaced out properly
    so that the blocks can be properly detected
    we also want to strip and leading or trailing whitespace
    finally , we add some newlines at the end to ensure proper padding 
    when parsing the content into blocks
    """
    # create and compile pattern
    NEWLINE_REPLACE_RAW = r'^\n{2,}'
    NEWLINE_REPLACE_PATTERN = re.compile(NEWLINE_REPLACE_RAW, re.MULTILINE | re.DOTALL)
    
    # replace the newlines
    processed_content = content.strip("\n ")
    processed_content = re.sub(NEWLINE_REPLACE_PATTERN, "\n", processed_content)
    
    # add new lines at the end for matcing purposes
    processed_content = processed_content + "\n\n"
    return processed_content


def tab_replace_content(content:str="")-> str:
    """
    replace the space between detected words with a new symbol
    """
    processed_content = re.sub(r'\t', " ", content)
    return processed_content


def remove_trailing_whitespace(content:str="")-> str:
    """
    replace the space between detected words with a new symbol
    """
    pattern_raw = r'\s+$'
    pattern = re.compile(pattern_raw, re.MULTILINE | re.DOTALL)
    processed_content = re.sub(pattern, "", content)
    return processed_content


def space_replace_content(content:str="")-> str:
    """
    replace the space between detected words with a new symbol
    """
    SPACE_REPLACE = r'(?:.{1})\s(?:.{1})'
    SPACE_REPLACE = r'(?=.)\s(?=.)'
    SPACE_REPLACE_PATTERN = re.compile(SPACE_REPLACE, re.MULTILINE)
    processed_content = re.sub(SPACE_REPLACE_PATTERN, "•", content)
    return processed_content



def extract_attrs(content:str="")-> str:
    """
    recieve a block of content that may have attributes
    we want to:
    - extract those attributes
    - return the content with the attributes removed
    """
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