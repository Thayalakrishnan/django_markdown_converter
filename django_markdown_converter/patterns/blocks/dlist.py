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
        
        ret = []
        # term
        term = data.get("term", "")
        ret.append(term)
        
        ## check here if the definition is a list or an
        definition = data.get("definition", "")
        if isinstance(definition, list):
            definition = [f": {_}" for _ in definition]
            ret.extend(definition)
        else:
            definition = f": {definition}"
            ret.append(definition)
        ret.append("")
        return "\n".join(ret)