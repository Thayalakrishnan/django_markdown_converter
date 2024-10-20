from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.data import HEADING_PATTERN


class HeadingPattern(Pattern):
    """
    heading
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="heading", pattern_object=HEADING_PATTERN, *args, **kwargs)
        
    def update_props(self):
        super().update_props()
        self.block["props"]["level"] = len(self.block["props"]["level"])
        
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        create_heading_lambda = lambda lvl, txt: f"{'#'*lvl} {txt}"
        
        props = self.block.get("props", {})
        level = props.get("level", 1)
        data = self.block.get("data", "")
        
        ret = []
        ret.append(create_heading_lambda(level, data))
        #ret.append(f"")
        return "\n".join(ret)