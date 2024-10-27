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


REGEX_FLAG_GROUP = lambda fs, pat: f"(?{fs}:{pat})"
REGEX_NAMED_GROUP = lambda name, pat: f"(?P<{name}>{pat})"
REGEX_GROUP = lambda pat: f"(?:{pat})"

def create_pattern_for_matching(label:str="", pattern_list:list=[], flags:str=""):
    pattern_parts_for_matching = []
    for p in pattern_list:
        if isinstance(p, str):
            pattern_parts_for_matching.append(p)
        else:
            pattern_parts_for_matching.append(REGEX_GROUP(p[1]))
    pattern_matching = "".join(pattern_parts_for_matching)
    pattern_matching = f"(?P<{label}>(?{flags}:{pattern_matching}))"
    return pattern_matching

def create_pattern_for_extracting(pattern_list:list=[], flags:str=""):
    pattern_parts_for_extracting = []
    for p in pattern_list:
        if isinstance(p, str):
            pattern_parts_for_extracting.append(p)
        else:
            pattern_parts_for_extracting.append(REGEX_NAMED_GROUP(p[0], p[1]))
    
    pattern_extracting = "".join(pattern_parts_for_extracting)
    pattern_extracting = re.compile(REGEX_FLAG_GROUP(flags, pattern_extracting))
    return pattern_extracting

class PatternAttributes:
    def __init__(self, pattern_attrs:dict=""):
        self.nested = pattern_attrs.get("nested", False)
        self.inlineMarkup = pattern_attrs.get("inlineMarkup", False)
        
class PatternProcessing:
    def __init__(self, pattern_attrs:dict=""):
        self.nested = pattern_attrs.get("nested", False)
        self.inlineMarkup = pattern_attrs.get("inlineMarkup", False)
        
    
class Pattern:
    #BLOCK_PATTERN, BLOCK_LOOKUP, PATTERN_LOOKUP
    PAT_PROPS_PATTERN = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
    PAT_BLOCK_PATTERN = []
    PAT_BLOCK_LOOKUP = {}
    PAT_PATTERN_LOOKUP = {}
    
    def __init__(self, pattern_obj:dict=""):
        self.type = pattern_obj.get("type", {})
        
        label = pattern_obj.get("type", {})
        flags = flag_setter(pattern_obj.get("flags", {}))
        pattern_list = pattern_obj.get("pattern", [])
        
        self.pattern_match = create_pattern_for_matching(label, pattern_list, flags) 
        self.pattern_extract = create_pattern_for_extracting(pattern_list, flags) 
        
        self.attributes = PatternAttributes(pattern_obj.get("attributes", {}))
        self.processing = ""
        
        self.PAT_BLOCK_PATTERN.append(self.pattern_match)
        self.PAT_BLOCK_LOOKUP[label] = self.pattern_extract
        #self.PAT_PATTERN_LOOKUP[label] = self
        self.PAT_PATTERN_LOOKUP[label] = pattern_obj
    
    
    @classmethod
    def build_lookups(cls):
        cls.PAT_BLOCK_PATTERN = REGEX_GROUP("|".join(cls.PAT_BLOCK_PATTERN))
        cls.PAT_BLOCK_PATTERN = re.compile(f"(?:{cls.PAT_BLOCK_PATTERN})" + cls.PAT_PROPS_PATTERN)
        #return block_pattern, block_lookup, pattern_lookup
        return cls.PAT_BLOCK_PATTERN, cls.PAT_BLOCK_LOOKUP, cls.PAT_PATTERN_LOOKUP
        


def create_patterns(label:str="", pattern_list:list=[], flags:str=""):
    pattern_parts_for_extracting = []
    pattern_parts_for_matching = []

    for p in pattern_list:
        if isinstance(p, str):
            pattern_parts_for_extracting.append(p)
            pattern_parts_for_matching.append(p)
        else:
            pattern_parts_for_extracting.append(REGEX_NAMED_GROUP(p[0], p[1]))
            pattern_parts_for_matching.append(REGEX_GROUP(p[1]))
    
    pattern_extracting = "".join(pattern_parts_for_extracting)
    pattern_extracting = re.compile(REGEX_FLAG_GROUP(flags, pattern_extracting))
    
    pattern_matching = "".join(pattern_parts_for_matching)
    pattern_matching = f"(?P<{label}>(?{flags}:{pattern_matching}))"
    
    return pattern_matching, pattern_extracting

def create_block_pattern():
    
    built_patterns = []
    block_lookup = {}
    pattern_lookup = {}

    for _ in PATTERNS:
        pattern_list = _["pattern"]
        label = _["type"]
        flags = flag_setter(_["flags"])
        
        ma_pattern, ex_pattern = create_patterns(label, pattern_list, flags)
        
        block_lookup[label] = ex_pattern
        built_patterns.append(ma_pattern)
        pattern_lookup[label] = _
        
        Pattern(_)
    
    
    props_pattern = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
    block_pattern = REGEX_GROUP("|".join(built_patterns))
    block_pattern = re.compile(f"(?:{block_pattern})" + props_pattern)
    
    #return block_pattern, block_lookup, pattern_lookup
    return Pattern.build_lookups()


BLOCK_PATTERN, BLOCK_LOOKUP, PATTERN_LOOKUP = create_block_pattern()

def extract_props(groupdict:dict={}) -> dict:
    props = groupdict.get("props", {})
    if props:
        props = convert_props(props)
    return props


def extract_block_and_attrs(groupdict:dict={}) -> dict:
    if groupdict["newline"]:
        return None
    
    # find the group that matched
    group = next((key for key,value in groupdict.items() if value), None)
    if not group:
        return None
    
    data = BLOCK_LOOKUP[group].match(groupdict[group]).groupdict()
    
    pattern = PATTERN_LOOKUP[group]
    attributes = pattern.get("attributes", {})
    
    # process attributes
    processing = pattern.get("processing", {})
    #if processing:
    for key, process in processing.items():
        data[key] = process(data[key])
    
    return {
        "type": group, 
        "props": extract_props(groupdict), 
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
    
    content = []
    for _ in tks:
        content.append(_)
        #print(repr(_["data"]))
        #print(_)
        #if _["type"]=="olist":
        #    print(repr(_["data"]["items"]))
    print(content)
    print(f"done")
    
run_new_mega_tokenizer_with_attrs_in_console()