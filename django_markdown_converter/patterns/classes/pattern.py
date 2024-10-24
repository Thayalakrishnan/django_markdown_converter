import re
from django_markdown_converter.helpers.processors import convert_props, process_input_content


def flag_setter(flags:dict={}):
    f = ""
    if flags["MULTILINE"]:
        f+= "m"
    if flags["DOTALL"]:
        f+= "s"
    return f


REGEX_GROUP_LABEL = lambda label, pat: f"(?P<{label}>{pat})"
REGEX_GROUP = lambda pat: f"(?:{pat})"
REGEX_FLAGS = lambda flags, pat: f"(?{flags}:{pat})"


def create_patterns(pattern):
    destructured_pattern = pattern["pattern"]
    label = pattern["type"]
    flags = flag_setter(pattern["flags"])

    pattern_check = []
    pattern_extract = []

    for p in destructured_pattern:
        if isinstance(p, str):
            pattern_check.append(p)
            pattern_extract.append(p)
        else:
            pattern_check.append(f"(?:{p[1]})")
            pattern_extract.append(REGEX_GROUP_LABEL(p[0], p[1]))
    
    pattern_extract = "".join(pattern_extract)
    #pattern_extract = re.compile(f"(?{flags}:{pattern_extract})")
    pattern_extract = re.compile(REGEX_FLAGS(flags, pattern_extract))
    
    pattern_check = "".join(pattern_check)
    #pattern_check = f"(?P<{label}>(?{flags}:{pattern_check}))"
    pattern_check = REGEX_GROUP_LABEL(label, REGEX_FLAGS(flags, pattern_check))
    
    return pattern_check, pattern_extract


class Pattern:
    
    def __init__(self, name:str="base", pattern_object:dict={}, manager=None, *args, **kwargs) -> None:
        self.name = name
        self.manager = manager
        
        self.blocktype = pattern_object["type"]
        self.pattern_check, self.pattern_extract = create_patterns(pattern_object["pattern"])
        
        self.hasNested = pattern_object["attributes"]["hasNested"]
        self.hasInline = pattern_object["attributes"]["hasInlineMarkup"]
        self.props = pattern_object["props"]
        self.data = pattern_object["data"]
    
        self.match = False
        self.block = None
        self.bank = []
        
    def __repr__(self) -> str:
        return self.name
    
    def check(self, block) -> bool:
        return self.pattern_check.match(block)
    
    def update_props(self):
        for p in self.props:
            if p == "data":
                continue
            if self.match.group(p):
                self.block["props"].update({p: self.match.group(p).strip()})
            if p == "attrs":
                attrs = convert_props(self.match.group("attrs"))
                self.block["props"].update(attrs)
                del self.block["props"]["attrs"]

    def get_props(self, props:str="") -> dict:
        if props:
            return convert_props(props)
        return {}
    
    def get_match(self, content):
        self.match = self.pattern_extract.match(content)
        
    def get_data(self) -> dict:
        if "data" in self.data:
            return self.match.group("data").strip()
        return {}
    
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        """
        the props can come in as:
        - curly braced enclosed attrs, after a block elelemt
        - a string of key value pairs from something like a XML element
        """
        #print(f"converting: {self.blocktype}")
        self.get_match(content)
        if not self.match:
            return {}
        self.block = {
            "type": self.blocktype,
            "props": self.get_props(props),
            "data": self.get_data()
        }
        self.update_props()
        self.add_to_bank()
        if self.hasNested:
            self.manager.block_converter(self.block)
        return self.block
    
    def add_to_bank(self, *args, **kwargs) -> None:
        if self.hasNested:
            self.bank.append(self.block)
            self.manager.PRIVATE_BANK.append(self.block)
    
    def revert(self, block:dict={}, *args, **kwargs) -> str:
        self.block = block
        #print(f"reverting: {self.blocktype}")
        return block["data"]
    
    def lookup_revert(self, block:dict={}) -> str:
        return self.manager.BLOCK_LOOKUP[block["type"]].revert(block)
    
    def lookup_convert(self, content:str="") -> dict:
        con = list(self.manager.block_parser(process_input_content(content)))
        if len(con) > 1:
            print(con)
            return con
        return [content]
