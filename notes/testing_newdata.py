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
    
    #print(block_lookup)
    
    props_pattern = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
    block_pattern = regex_group("|".join(built_patterns))
    block_pattern = re.compile(f"(?:{block_pattern})" + props_pattern)
    
    return block_pattern, block_lookup


BLOCK_PATTERN, BLOCK_LOOKUP = create_block_pattern()


def extract_block_and_attrs(groupdict:dict={}) -> dict:
    block = {"type": None, "props": None, "data": None}
    
    if groupdict["newline"]:
        return None
    
    for k,v in groupdict.items():
        if v:
            block["type"] = k
            block["data"] = v
            block["data"] = BLOCK_LOOKUP[k].match(v).groupdict()
            break
        
    if groupdict["props"]:
        props = groupdict.get("props", None)
        if props:
            block["props"] = convert_props(props)
    return block


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