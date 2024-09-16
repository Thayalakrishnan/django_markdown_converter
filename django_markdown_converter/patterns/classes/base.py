import re

from django_markdown_converter.helpers.processors import process_props

class BasePattern:
    
    def __init__(self, pattern_object:dict={}, *args, **kwargs) -> None:
        self.blocktype = pattern_object["type"]
        
        self.check_pattern = re.compile(pattern_object["check"], re.MULTILINE | re.DOTALL)
        self.pattern = re.compile(pattern_object["pattern"], pattern_object["flags"])
        
        self.hasNested = pattern_object["hasNested"]
        self.hasInline = pattern_object["hasInlineMarkup"]
        
        self.props = pattern_object["props"]
        self.data = pattern_object["data"]
    
        self.match = False
        self.block = None

    def check(self, block) -> bool:
        return self.check_pattern.match(block)
    
    def update_props(self):
        for p in self.props:
            if p == "data":
                continue
            if self.match.group(p):
                self.block["props"].update({p: self.match.group(p)})

    def get_props(self, props:str="") -> dict:
        if props:
            return process_props(props)
        return {}
    
    def get_match(self, content):
        self.match = self.pattern.match(content)
        
    def get_data(self) -> dict:
        if "data" in self.data:
            return self.match.group("data")
        return {}
            
    def convert(self, content, props, *args, **kwargs) -> dict:
        """ """
        print(f"converting: {self.blocktype}")
        self.get_match(content)
        self.block = {
            "type": self.blocktype,
            "props": self.get_props(props),
            "data": self.get_data()
        }
        self.update_props()
        return self.block


def metavalues(data):
    return

def dedent(data):
    data = data.split("\n")
    data = [_.lstrip(" ") for _ in data]
    return "\n".join(data)


def count(data):
    return len(data)

def deprefix(data, prefix):
    data = data.split("\n")
    data = [_.lstrip(prefix) for _ in data]
    return data
