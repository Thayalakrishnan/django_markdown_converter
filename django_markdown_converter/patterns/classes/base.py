import re

from django_markdown_converter.helpers.processors import process_props

class BasePattern:
    
    def __init__(self, pattern_object:dict={}, *args, **kwargs) -> None:
        self.blocktype = pattern_object["type"]
        self.check_pattern = re.compile(pattern_object["check"], re.MULTILINE | re.DOTALL)
        self.pattern = re.compile(pattern_object["pattern"], pattern_object["flags"])
        self.process = pattern_object["process"]
        self.hasNested = pattern_object["hasNested"]
        self.hasInline = pattern_object["hasInlineMarkup"]
        self.props = pattern_object["props"]

    def check(self, block) -> bool:
        return self.check_pattern.match(block)
    
    def get_props(self, props:str="") -> dict:
        if props:
            return process_props(props)
        return {}
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        """ """
        block = {
            "type": self.blocktype,
            "props": self.get_props(props),
            "data": content
        }
        return block


class OneShotPattern(BasePattern):
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            if "data" in self.props:
                block["data"] = m.group("data")
            else:
                block["data"] = m.groupdict()
            for p in self.props:
                if p == "data":
                    continue
                block["props"].update({p: m.group(p)})
        return block


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