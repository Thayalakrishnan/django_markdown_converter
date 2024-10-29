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
        self.inlinemarkup = pattern_attrs.get("inlinemarkup", False)


class Pattern:
    NESTED_BANK = []
    
    def __init__(self, manager:str=None, pattern_obj:dict={}):
        self.manager = manager
        self.name = pattern_obj.get("name", "")
        self.processing = pattern_obj.get("processing", {})
        self.data_key = pattern_obj.get("data", "content")
        self.attributes = PatternAttributes(pattern_obj.get("attributes", {}))
        self.flags = flag_setter(pattern_obj.get("flags", {}))
        
        self.BANK = []
        
        pattern_list = pattern_obj.get("pattern", [])
        
        self.groups = [p[0] for p in pattern_list if isinstance(p, tuple)]
        self.matching = create_pattern_for_matching(self.name, pattern_list, self.flags) 
        self.extracting = create_pattern_for_extracting(self.name, pattern_list, self.flags)

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
    
    def get_block(self, groupdict:dict={}) -> dict:
        props = self.get_props(groupdict)
        #data = self.get_data(groupdict)
        ret = self.get_data(groupdict)
        
        self.process_data(ret)
        
        data = ret.pop(self.data_key)
        
        if ret:
            if props:
                ret.update(props)
        
        block = {
            "name": self.name,
            "props": ret,
            "data": data,
        }
        return block
    
    def convert(self, groupdict:dict={}) -> dict:
        block = self.get_block(groupdict)
        self.BANK.append(block)
        if self.attributes.nested:
            self.NESTED_BANK.append(block)
            block["data"] = self.manager.nested_convert(block["data"])
        return block


class Manager:
    
    def __init__(self, patterns:list=[]):
        self.props_pattern = r"(?m:^\{ *?(?P<props>.*?) *?\}\n)?"
        self.block_pattern = []
        self.pattern_lookup = {}
        self.BANK = []
        
        for _ in patterns:
            self.add_pattern(_)
            
        self.block_pattern = REGEX_GROUP("|".join(self.block_pattern))
        self.block_pattern = re.compile(f"(?:{self.block_pattern})" + self.props_pattern)
    
    def add_pattern(self, pattern_obj:dict={}):
        pattern = Pattern(self, pattern_obj) 
        self.block_pattern.append(pattern.matching)
        self.pattern_lookup[pattern.name] = pattern
    
    @staticmethod
    def get_name(groupdict:dict={}) -> dict:
        if groupdict["newline"]:
            return ""
        if groupdict["none"]:
            return ""
        # find the group that matched
        name = next((key for key,value in groupdict.items() if value), None)
        if not name:
            return ""
        return name
    
    def get_pattern(self, name:str="") -> Pattern:
        return self.pattern_lookup[name]

    def get_block(self, name:str="", groupdict:dict={}) -> dict:
        pattern = self.get_pattern(name)
        block = pattern.convert(groupdict)
        self.BANK.append(block)
        return block
    
    def get_matches(self, source:str=""):
        matches = self.block_pattern.finditer(source)
        for match in matches:
            groupdict = match.groupdict()
            name = self.get_name(groupdict)
            if name:
                yield self.get_block(name, groupdict)
    
    def nested_convert(self, source) -> list:
        if isinstance(source, list):
            for item in source:
                item["data"] = self.nested_convert(item["data"])
            return source
        elif isinstance(source, str):
            return self.convert(source)
    
    def convert(self, source:str="") -> list:
        blocks = []
        matches = self.get_matches(source)
        for _ in matches:
            blocks.append(_)
        if len(blocks):
            return blocks
        return source
    
    def tokenize(self, source:str=""):
        matches = self.block_pattern.finditer(source)
        for match in matches:
            groupdict = match.groupdict()
            name = self.get_name(groupdict)
            if name:
                yield name
                
    def loop_over_nested_blocks(self):
        for _ in Pattern.NESTED_BANK:
            print(_)


def run_new_mega_tokenizer_with_attrs_in_console():
    PATH_TO_FILE = "notes/examples/small/markdown.md"
    PATH_TO_FILE = "notes/examples/list/markdown.md"
    source = get_source(PATH_TO_FILE)
    pm = Manager(PATTERNS)
    converted = pm.convert(source)
    print(converted)
    print("NESTED --------------------------------------")
    pm.loop_over_nested_blocks()
    print(f"done")
    


run_new_mega_tokenizer_with_attrs_in_console()


#PM = Manager(PATTERNS)
#
#def run_new_mega_tokenizer_with_attrs(source:str=""):
#    #pm = Manager(PATTERNS)
#    tokens = PM.tokenize(source)
#    for _ in tokens:
#        yield _