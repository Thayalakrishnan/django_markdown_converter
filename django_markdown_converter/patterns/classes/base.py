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
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        """ """
        block = {
            "type": self.blocktype,
            "props": process_props(props),
            "data": content
        }
        return block

        
class FindAllPattern(BasePattern):
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        ## findall
        if self.process == "findall":
            m = self.pattern.findall(content)
            if m:
                if self.blocktype == "blockquote":
                    m = [_.lstrip(" ") for _ in m]
                    block["data"] = "".join(m)
                else:
                    block["data"] = m
        return block


class HeaderBodyPattern(BasePattern):
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        if self.process == "headerbody":
            m = self.pattern.match(content)
            if m:
                if self.blocktype == "dlist":
                    block["data"] = m.groupdict()
                    definition = m.group("definition").split("\n")
                    definition = [_.lstrip(": ") for _ in definition]
                    block["data"]["definition"] = definition
                elif self.blocktype == "footnote" or self.blocktype == "admonition":
                    data = m.group("data").split("\n")
                    data = [_.lstrip(" ") for _ in data]
                    block["data"] = "\n".join(data)
                    
                    for p in self.props:
                        if p == "data":
                            continue
                        block["props"].update({p: m.group(p)})
                        
                elif self.blocktype == "table":
                    block["data"] = {}
                    for p in self.props:
                        if p == "data":
                            continue
                        block["data"].update({p: m.group(p)})
                else:
                    block["data"] = m.groupdict()
        return block
    


class OneShotPattern(BasePattern):
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        if self.process == "oneshot":
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


class CaptureProcessPattern(BasePattern):
    
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        if self.process == "captureprocess":
            m = self.pattern.match(content)
            if m:
                block["data"] = m.group("data")
                for p in self.props:
                    if p == "data":
                        continue
                    block["props"].update({p: m.group(p)})
            
        return block
    
    
