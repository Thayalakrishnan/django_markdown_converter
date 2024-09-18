from django_markdown_converter.patterns.classes.base import BasePattern


class HeadingPattern(BasePattern):
    """
    heading
    """
    
    def update_props(self):
        super().update_props()
        self.block["props"]["level"] = len(self.block["props"]["level"])
        
    def revert(self, *args, **kwargs) -> str:
        block = super().revert(*args, **kwargs)
        create_heading_lambda = lambda lvl, txt: f"{'#'*lvl} {txt}"
        
        props = block.get("props", {})
        level = props.get("level", 1)
        data = block.get("data", "")
        
        ret = []
        ret.append(create_heading_lambda(level, data))
        ret.extend(data)
        ret.append(f"")
        return "\n".join(ret)