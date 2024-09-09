import re


def process_input_content(content:str="")-> str:
    """
    transform the content by replacing multiple newline characters
    with a single newline character. 
    essentially we wan to ensure that the content is spaced out properly
    so that the blocks can be properly detected
    we also want to strip some of the leading or trailing whitespace
    but not sure if it will work well due to line breaks in multi-line blocks and nested blocks
    - for example admonitions which may have nested line breaks will lose their lines inbetween, as well list blocks
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
    content = content.strip(" \n")
    processed_content = re.sub(r'\t', " ", content)
    return processed_content


def remove_trailing_whitespace(content:str="")-> str:
    """
    replace the space between detected words with a new symbol
    """
    content = content.strip(" \n")
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

def excise(content:str="", target:str="", before:str="(?P<before>.*)", after:str="(?P<after>.*)")-> tuple[str, str]:
    """
    given a regex pattern, we want to:
    - scan the pattern
    - excise the content if present
    - return content and the excised bit
    """
    pattern_raw = f'{before}{target}{after}'
    pattern = re.compile(pattern_raw, re.MULTILINE | re.DOTALL)
    match = pattern.match(content)
    
    if match:
        return match.group(1).strip() + match.group(3).strip(), match.group(2)
    return content, ""


def excise_props(content:str="")-> str:
    """
    recieve a block of content that may have attributes
    we want to:
    - extract those attributes
    - return the content with the attributes removed
    """
    return excise(content=content, target=r'\{(?P<props>.*?)\}', after="(?P<after>$)")


def process_meta_block(meta:str="")-> dict:
    """
    recieve a meta block
    we want to:
    - extract the attributes
    - return the content with the attributes removed
    - return a dict with the values from the metablock as a dict
    and the extracted props merged
    """
    kvs_dict = {}
    meta, props = excise_props(content=meta)
    props = process_props(props)
    
    if props:
        kvs_dict.update(props)
        
    PATTERN_RAW = r'^---(?P<data>.*?)\n^---'
    pattern = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)
    match = pattern.match(meta)
    
    if match:
        data = match.group("data").strip()
        
        if not data:
            return kvs_dict
        
        lines = data.split("\n")
        
        if not lines:
            return kvs_dict
        
        kvs = process_meta_values(data)
        
        if kvs:
            kvs_dict.update(dict(kvs))
            return kvs_dict
    return kvs_dict

def extract_meta_block(content:str="")-> str:
    """
    recieve a block of content that may have a meta block
    - check if there is a metablock
    - if there is, extract it
        - check for attached props, excise them and process them
        - process the meta block to extract its key value pairs
    - create the meta block
    - return the meta block and the content without the meta
    """
    processed_content, meta = excise(content=content, target=r'(?P<target>(?:^---.*?\n^\n))', before="(?P<before>.*?)", after="(?P<after>.*)")
    processed_content = processed_content + "\n\n"
    return processed_content, process_meta_block(meta)

def process_meta_values(content:str="")-> dict:
    """
    receive the innards of a meta block 
    process this data and return key value pairs as a dict
    always returnsa  dict
    the pattern will only select key value pairs
    each match will return a tuple that can then create a dictionary
    meta keys must be unique
    """
    PATTERN_RAW = r'^(?P<key>.*?)(?:\:\s*)(?P<value>.*?)(?:\n|$)'
    PATTERN = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)
    kvps = PATTERN.findall(content)
    if kvps:
        return dict(kvps)
    return {}

def process_props(props:str="")-> dict:
    """
    receive a string that represents key value pairs
    we want to:
    - extract those attributes
    - return them as a dict
    """
    PATTERN_RAW = r'(\S*?)\=(\".*?\")|(\S*?)\=(\'.*?\')'
    PATTERN_RAW = r'(\S*?)\=(?P<open>[\"\'])(.*?)(?P=open)'
    props = props.strip()
    vals = re.findall(PATTERN_RAW, props, re.MULTILINE | re.DOTALL)
    vals = [(_[0], _[2]) for _ in vals]
    return dict(vals)