import re
from django_markdown_converter.patterns.newdata import PATTERNS
from django_markdown_converter.helpers.processors import convert_props, process_input_content
from notes.tools import get_source
from typing import Callable

def flag_setter(flags:dict={}):
    f = ""
    if flags["MULTILINE"]:
        f+= "m"
    if flags["DOTALL"]:
        f+= "s"
    return f

REGEX_FLAG_GROUP = lambda flags, pat: f"(?{flags}:{pat})"
REGEX_NAMED_GROUP = lambda name, pat: f"(?P<{name}>{pat})"
REGEX_GROUP = lambda pat: f"(?:{pat})"
REGEX_NAMED_FLAG_GROUP = lambda name, flags, pat: REGEX_NAMED_GROUP(name, REGEX_FLAG_GROUP(flags, pat))

def create_pattern_generic(name:str="", pattern_list:list=[], flags:str="", named:bool=False, group_names:bool=False):
    pattern_parts = ""
    for p in pattern_list:
        if isinstance(p, str):
            pattern_parts+=p
        else:
            if group_names:
                pattern_parts+=REGEX_NAMED_GROUP(p[0], p[1])
            else:
                pattern_parts+=REGEX_GROUP(p[1])
    if named:
        ## pattern matching
        return REGEX_NAMED_FLAG_GROUP(name, flags, pattern_parts)
    ## pattern extracting
    return re.compile(REGEX_FLAG_GROUP(flags, pattern_parts))


def create_pattern_for_matching(name:str="", pattern_list:list=[], flags:str=""):
    return create_pattern_generic(name, pattern_list, flags, named=True, group_names=False)

def create_pattern_for_extracting(name:str="", pattern_list:list=[], flags:str=""):
    return create_pattern_generic(name, pattern_list, flags, named=False, group_names=True)

class PatternAttributes:
    def __init__(self, pattern_attrs:dict=""):
        self.nested = pattern_attrs.get("nested", False)
        self.inlineMarkup = pattern_attrs.get("inlineMarkup", False)
        
class Pattern:
    def __init__(self, name:str="", pattern_list:list=[], flags:str=""):
        self.name = name
        self.pattern_list = pattern_list
        self.flags = flags
        self.groups = [p[0] for p in pattern_list if isinstance(p, tuple)]
        
        self.matching = create_pattern_for_matching(name, pattern_list, flags) 
        self.extracting = create_pattern_for_extracting(name, pattern_list, flags) 

        
class PatternManager:
    PROPS_PATTERN = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
    BLOCK_PATTERN = []
    INSTANCE_LOOKUP = {}
    
    def __init__(self, pattern_obj:dict=""):
        self.manager = None
        self.type = pattern_obj.get("type", {})
        self.attributes = PatternAttributes(pattern_obj.get("attributes", {}))
        self.processing = pattern_obj.get("processing", {})
        
        name = pattern_obj.get("type", {})
        flags = flag_setter(pattern_obj.get("flags", {}))
        pattern_list = pattern_obj.get("pattern", [])
        
        pattern_match = create_pattern_for_matching(name, pattern_list, flags) 
        self.pattern_extract = create_pattern_for_extracting(name, pattern_list, flags) 
        
        self.BLOCK_PATTERN.append(pattern_match)
        self.INSTANCE_LOOKUP[name] = self
        
    @classmethod
    def build_lookups(cls):
        cls.BLOCK_PATTERN = REGEX_GROUP("|".join(cls.BLOCK_PATTERN))
        cls.BLOCK_PATTERN = re.compile(f"(?:{cls.BLOCK_PATTERN})" + cls.PROPS_PATTERN)
    
    def get_props(self, groupdict:dict={}) -> dict:
        props = groupdict.get("props", {})
        if props:
            props = convert_props(props)
        return props
    
    def get_data(self, groupdict:dict={}) -> dict:
        match = self.pattern_extract.match(groupdict[self.type])
        if match:
            return match.groupdict()
        return {}
    
    def process_data(self, data:dict={}) -> dict:
        for key, process in self.processing.items():
            data[key] = process(data[key])
    
    def convert(self, groupdict:dict={}) -> dict:
        props = self.get_props(groupdict)
        data = self.get_data(groupdict)
        self.process_data(data)
        return {
            "type": self.type,
            "props": props,
            "data": data,
        }

#def create_block_pattern():
#    for _ in PATTERNS:
#        PatternManager(_)
#    PatternManager.build_lookups()
#create_block_pattern()


def extract_block_and_attrs(groupdict:dict={}) -> dict:
    if groupdict["newline"]:
        return None
    # find the group that matched
    group = next((key for key,value in groupdict.items() if value), None)
    if not group:
        return None
    return PatternManager.INSTANCE_LOOKUP[group].convert(groupdict)


def run_my_mega_tokenizer_with_attrs(source:str=""):
    
    for _ in PATTERNS:
        PatternManager(_)
    PatternManager.build_lookups()
    
    #matches = re.finditer(PatternManager.BLOCK_PATTERN, source)
    matches = PatternManager.BLOCK_PATTERN.finditer(source)
    for _ in matches:
        block = extract_block_and_attrs(_.groupdict())
        if block:
            yield block

def run_new_mega_tokenizer_with_attrs_in_console():
    PATH_TO_FILE = "notes/examples/small/markdown.md"
    source = get_source(PATH_TO_FILE)
    tks = run_my_mega_tokenizer_with_attrs(source)
    
    content = []
    for _ in tks:
        content.append(_)
    print(content)
    print(f"done")
    
run_new_mega_tokenizer_with_attrs_in_console()










#def run_new_mega_tokenizer_with_attrs(source:str=""):
#    matches = re.finditer(PatternManager.BLOCK_PATTERN, source)
#    for _ in matches:
#        block = extract_block_and_attrs(_.groupdict())
#        if block:
#            yield block