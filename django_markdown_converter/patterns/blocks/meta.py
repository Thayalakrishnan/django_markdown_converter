import re
from django_markdown_converter.patterns.classes.base import BasePattern


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
    def get_data(self) -> dict:
        data = self.match.group("data").strip()
        
        lines = data.split("\n")
        if not lines:
            return None
        
        kvs = process_meta_values(data)
        
        if kvs:
            return kvs
        return None
