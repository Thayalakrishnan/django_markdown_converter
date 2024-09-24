from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import DLIST_PATTERN


class DListPattern(BasePattern):
    """
    props:
    - index
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("dlist", DLIST_PATTERN, *args, **kwargs)
        
    def get_data(self) -> dict:
        definition = self.match.group("definition").split("\n")
        definition = [_.lstrip(": ") for _ in definition]
        definition = [_ for _ in definition if len(_)]
        term = self.match.group("term").strip("\n ")
        return {
            "term": term,
            "definition": definition,
        }


    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        props = self.block.get("props", {})
        data = self.block.get("data", "")
        
        term = data.get("term", "")
        definition = data.get("definition", [""])
        definition = [f": {_}" for _ in definition]
        
        ret = []
        ret.append(term)
        ret.extend(definition)
        ret.append("")
        return "\n".join(ret)