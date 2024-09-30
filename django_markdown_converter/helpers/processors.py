import re

def process_input_content(content:str="")-> str:
    """
    transform the content by replacing multiple newline characters
    with a single newline character. 
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


def convert_props(props:str="")-> dict:
    """
    receive a string that represents key value pairs
    return them as a dict
    """
    PATTERN_RAW = r'(\S*?)\=(?P<open>[\"\'])(.*?)(?P=open)'
    props = props.strip()
    vals = re.findall(PATTERN_RAW, props, re.MULTILINE | re.DOTALL)
    vals = [(_[0], _[2]) for _ in vals]
    return dict(vals)


def revert_props(props:dict={})-> str:
    """
    receive a props object, return the props as attrs in string form
    """
    items = props.items()
    if not items:
        return ""
    joined_items = " ".join([f'{prop[0]}="{prop[1]}"' for prop in items])
    return f" {joined_items} "