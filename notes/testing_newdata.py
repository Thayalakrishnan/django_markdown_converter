import re
from django_markdown_converter.patterns.newdata import PATTERNS
from notes.tools import get_source


def flag_setter(flags:dict={}):
    f = ""
    if flags["MULTILINE"]:
        f+= "m"
    if flags["DOTALL"]:
        f+= "s"
    return f

def create_block_pattern():
    #regex_named_group = lambda name, pat: f"(?P<{name}>{pat})"
    regex_group = lambda pat: f"(?:{pat})"
    
    built_patterns = []

    for _ in PATTERNS:
        pattern_list = _["pattern"]
        label = _["type"]
        flags = flag_setter(_["flags"])

        pattern_parts = []

        for p in pattern_list:
            if isinstance(p, str):
                pattern_parts.append(p)
                continue
            else:
                pattern_parts.append(f"(?:{p[1]})")
        pattern = "".join(pattern_parts)
        current_pattern = f"(?P<{label}>(?{flags}:{pattern}))"
        built_patterns.append(current_pattern)

    props_pattern = r"(?m:(?P<props>^\{.*?\}\n))?"
    block_pattern = regex_group("|".join(built_patterns))
    block_pattern = re.compile(f"(?:{block_pattern})" + props_pattern)
    
    return block_pattern


def extract_block_and_attrs(groupdict:dict={}) -> dict:
    token = ""
    if groupdict["newline"]:
        return token, {}
    ret = {}
    for k,v in groupdict.items():
        if v:
            ret[k] = v
            token = k
            break

    if "props" in groupdict:
        ret["props"] = groupdict.get("props", None)
    return token, ret


BLOCK_PATTERN = create_block_pattern()

def run_new_mega_tokenizer_with_attrs(source:str=""):
    matches = re.finditer(BLOCK_PATTERN, source)
    for _ in matches:
        token, block = extract_block_and_attrs(_.groupdict())
        if token:
            yield token


def run_new_mega_tokenizer_with_attrs_in_console():
    PATH_TO_FILE = "notes/examples/post.md"
    source = get_source(PATH_TO_FILE)
    tks = run_new_mega_tokenizer_with_attrs(source)
    for _ in tks:
        print(_)
        
    print(f"done")
    
#run_new_mega_tokenizer_with_attrs_in_console()