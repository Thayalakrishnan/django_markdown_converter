import re
from django_markdown_converter.patterns.newdata import PATTERNS
from django_markdown_converter.helpers.processors import convert_props, process_input_content
from notes.tools import get_source


def flag_setter(flags:dict={}):
    f = ""
    if flags["MULTILINE"]:
        f+= "m"
    if flags["DOTALL"]:
        f+= "s"
    return f


def create_block_pattern():
    regex_named_group = lambda name, pat: f"(?P<{name}>{pat})"
    regex_group = lambda pat: f"(?:{pat})"
    
    built_patterns = []
    block_lookup = {}
    pattern_lookup = {}

    for _ in PATTERNS:
        pattern_list = _["pattern"]
        label = _["type"]
        flags = flag_setter(_["flags"])

        pattern_parts_extraction = []
        pattern_parts_for_block_pattern = []

        for p in pattern_list:
            if isinstance(p, str):
                pattern_parts_extraction.append(p)
                pattern_parts_for_block_pattern.append(p)
                continue
            else:
                pattern_parts_extraction.append(regex_named_group(p[0], p[1]))
                pattern_parts_for_block_pattern.append(f"(?:{p[1]})")
        
        ex_pattern = "".join(pattern_parts_extraction)
        block_lookup[label] = re.compile(f"(?{flags}:{ex_pattern})")
        
        pattern = "".join(pattern_parts_for_block_pattern)
        current_pattern = f"(?P<{label}>(?{flags}:{pattern}))"
        built_patterns.append(current_pattern)
        pattern_lookup[label] = _
    
    #print(block_lookup)
    
    props_pattern = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
    block_pattern = regex_group("|".join(built_patterns))
    block_pattern = re.compile(f"(?:{block_pattern})" + props_pattern)
    
    return block_pattern, block_lookup, pattern_lookup


BLOCK_PATTERN, BLOCK_LOOKUP, PATTERN_LOOKUP = create_block_pattern()


def extract_block_and_attrs(groupdict:dict={}) -> dict:
    if groupdict["newline"]:
        return None
    
    group = next((key for key,value in groupdict.items() if value), None)
    if not group:
        return None
    
    data = BLOCK_LOOKUP[group].match(groupdict[group]).groupdict()
    
    # process attributes
    processing = PATTERN_LOOKUP[group].get("processing", None)
    
    if processing:
        for process in processing.keys():
            data[process] = processing[process](data[process])
    
    #if groupdict["props"]:
    props = groupdict.get("props", {})
    if props:
        props = convert_props(props)
    return {
        "type": group, 
        "props": props, 
        "data": data
    }


def run_new_mega_tokenizer_with_attrs(source:str=""):
    matches = re.finditer(BLOCK_PATTERN, source)
    for _ in matches:
        block = extract_block_and_attrs(_.groupdict())
        if block:
            yield block
            
def run_my_mega_tokenizer_with_attrs(source:str=""):
    matches = re.finditer(BLOCK_PATTERN, source)
    for _ in matches:
        block = extract_block_and_attrs(_.groupdict())
        if block:
            yield block

def run_new_mega_tokenizer_with_attrs_in_console():
    PATH_TO_FILE = "notes/examples/post.md"
    source = get_source(PATH_TO_FILE)
    tks = run_my_mega_tokenizer_with_attrs(source)
    for _ in tks:
        print(repr(_["data"]))
    print(f"done")
    
run_new_mega_tokenizer_with_attrs_in_console()