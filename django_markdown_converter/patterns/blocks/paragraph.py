from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.inlines.parser import inline_parser

INLINE_TAG_LOOKUP = {
    ## symetrical
    "text": lambda x: f"{x}",
    "email": lambda x: f"<{x}>",
    "code": lambda x: f"`{x}`",
    "strong": lambda x: f"**{x}**",
    "em": lambda x: f"*{x}*",
    "del": lambda x: f"*~~{x}~~",
    "mark": lambda x: f"=={x}==",
    "samp": lambda x: f"``{x}``",
    "emoji": lambda x: f":{x}:",
    "sup": lambda x: f"^{x}^",
    "sub": lambda x: f"~{x}~",
    "math": lambda x: f"${x}$",
    ## not
    "footnote": lambda x: f"[^{x}]",
    "link": lambda x,y: f"[{x}]({y})",
}


def loop_recursion(subblocks:list=[]) -> str:
    fragments = []
    for subblock in subblocks:
        if isinstance(subblock["data"], str):
            fragments.append(INLINE_TAG_LOOKUP[subblock["tag"]](subblock["data"]))
        else:
            subblock["data"] = loop_recursion(subblock["data"])
            fragments.append(INLINE_TAG_LOOKUP[subblock["tag"]](subblock["data"]))
    return "".join(fragments)


class ParagraphPattern(BasePattern):
    
    def convert(self, content:str="", props:str="", *args, **kwargs) -> dict:
        super().convert(content, props, *args, **kwargs)
        self.block["data"] = inline_parser(self.block["data"])
        return self.block
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        data = self.block.get("data", "")
        
        if isinstance(data, str):
            ret = []
            ret.append(data)
            ret.append("")
            return "\n".join(ret)
        else:
            #p = [INLINE_TAG_LOOKUP[subblock["tag"]](subblock["data"]) for subblock in data]
            #p.append("\n")
            #return "".join(p)
            p = [loop_recursion(data)]
            p.append("\n")
            return "".join(p)