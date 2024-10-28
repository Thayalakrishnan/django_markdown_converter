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
    def __init__(self, manager:str=None, name:str="", pattern_list:list=[], flags:str="", processing:dict={},attributes:PatternAttributes=None):
        self.manager = manager
        self.name = name
        self.groups = [p[0] for p in pattern_list if isinstance(p, tuple)]
        self.matching = create_pattern_for_matching(name, pattern_list, flags) 
        self.extracting = create_pattern_for_extracting(name, pattern_list, flags)
        self.processing = processing
        self.attributes = attributes

    @staticmethod
    def get_props(groupdict:dict={}) -> dict:
        props = groupdict.get("props", {})
        if props:
            props = convert_props(props)
        return props
    
    def get_data(self, groupdict:dict={}) -> dict:
        match = self.extracting.match(groupdict[self.name])
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
            "name": self.name,
            "props": props,
            "data": data,
        }

class Manager:
    
    def __init__(self, patterns:list=[]):
        self.PROPS_PATTERN = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
        self.BLOCK_PATTERN = []
        self.PATTERN_LOOKUP = {}
        self.BANK = []
        
        for _ in patterns:
            self.add_pattern(_)
            
        self.BLOCK_PATTERN = REGEX_GROUP("|".join(self.BLOCK_PATTERN))
        self.BLOCK_PATTERN = re.compile(f"(?:{self.BLOCK_PATTERN})" + self.PROPS_PATTERN)
    
    def add_pattern(self, pattern_obj:dict={}):
        name = pattern_obj.get("name", "")
        attributes = PatternAttributes(pattern_obj.get("attributes", {}))
        processing = pattern_obj.get("processing", {})
        flags = flag_setter(pattern_obj.get("flags", {}))
        pattern_list = pattern_obj.get("pattern", [])
        pattern = Pattern(self, name, pattern_list, flags, processing, attributes) 
        self.BLOCK_PATTERN.append(pattern.matching)
        self.PATTERN_LOOKUP[name] = pattern
    
    @staticmethod
    def get_name(groupdict:dict={}) -> dict:
        if groupdict["newline"]:
            return ""
        # find the group that matched
        name = next((key for key,value in groupdict.items() if value), None)
        if not name:
            return ""
        return name
    
    def get_pattern(self, name:str="") -> Pattern:
        return self.PATTERN_LOOKUP[name]

    def get_block(self, name:str="", groupdict:dict={}) -> dict:
        pattern = self.get_pattern(name)
        block = pattern.convert(groupdict)
        
        return block
    
    def get_matches(self, source:str=""):
        matches = self.BLOCK_PATTERN.finditer(source)
        for match in matches:
            groupdict = match.groupdict()
            name = self.get_name(groupdict)
            if name:
                yield self.get_block(name, groupdict)
    
    def convert(self, source:str="") -> list:
        blocks = []
        matches = self.get_matches(source)
        for _ in matches:
            blocks.append(_)
            
        return blocks
    
    def tokenize(self, source:str=""):
        matches = self.BLOCK_PATTERN.finditer(source)
        for match in matches:
            groupdict = match.groupdict()
            name = self.get_name(groupdict)
            if name:
                yield name



def run_new_mega_tokenizer_with_attrs_in_console():
    PATH_TO_FILE = "notes/examples/small/markdown.md"
    source = get_source(PATH_TO_FILE)
    pm = Manager(PATTERNS)
    converted = pm.convert(source)
    print(converted)
    print(f"done")
    

run_new_mega_tokenizer_with_attrs_in_console()

PM = Manager(PATTERNS)

def run_new_mega_tokenizer_with_attrs(source:str=""):
    #pm = Manager(PATTERNS)
    tokens = PM.tokenize(source)
    for _ in tokens:
        yield _