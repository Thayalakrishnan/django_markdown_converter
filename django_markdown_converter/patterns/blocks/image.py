from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import IMAGE_PATTERN


class ImagePattern(BasePattern):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("image", IMAGE_PATTERN, *args, **kwargs)

    def revert(self, *args, **kwargs) -> str:
        create_image_lambda = lambda a, s, t: f"![{a}]({s} \"{t}\")" if len(t) else f"![{a}]({s})"
        super().revert(*args, **kwargs)
        
        props = self.block.get("props", {})
        
        alt = props.get("alt", "")
        title = props.get("title", "")
        src = self.block.get("data", "")
        
        ret = []
        ret.append(create_image_lambda(alt, src, title))
        ret.append("")
        return "\n".join(ret)