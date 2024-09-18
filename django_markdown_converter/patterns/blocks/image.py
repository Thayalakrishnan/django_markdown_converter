from django_markdown_converter.patterns.classes.base import BasePattern


class ImagePattern(BasePattern):
    pass

    def revert(self, *args, **kwargs) -> str:
        create_image_lambda = lambda a, s, t: f"![{a}]({s} \"{t}\")" if len(t) else f"![{a}]({s})"
        block = super().revert(*args, **kwargs)
        
        props = block.get("props", {})
        
        alt = props.get("alt", "")
        title = props.get("title", "")
        src = block.get("data", "")
        
        ret = []
        ret.append(create_image_lambda(alt, src, title))
        ret.append("")
        return "\n".join(ret)