import re
from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import META_PATTERN


def process_meta_values(content:str="")-> dict:
    """
    receive the innards of a meta block 
    process this data and return key value pairs as a dict
    always returnsa  dict
    the pattern will only select key value pairs
    each match will return a tuple that can then create a dictionary
    meta keys must be unique
    """
    PATTERN_RAW = r'^(?P<key>.*?)(?:\:\s*)(?P<value>.*?)(?:\n|$)'
    PATTERN = re.compile(PATTERN_RAW, re.MULTILINE | re.DOTALL)
    kvps = PATTERN.findall(content)
    if kvps:
        return dict(kvps)
    return {}


class MetaPattern(BasePattern):
    """
    meta
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("meta", META_PATTERN, *args, **kwargs)
        
    def get_data(self) -> dict:
        data = self.match.group("data").strip()
        
        lines = data.split("\n")
        if not lines:
            return None
        
        kvs = process_meta_values(data)
        
        if kvs:
            return kvs
        return None

    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        data = self.block.get("data", "")
        middle = [f"{key}: {data[key]}" for key in data]
        
        ret = []
        ret.append("---")
        ret.extend(middle)
        ret.append("---")
        return "\n".join(ret)