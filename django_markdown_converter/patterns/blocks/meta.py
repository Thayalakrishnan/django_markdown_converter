from django_markdown_converter.patterns.classes.base import BasePattern


class MetaPattern(BasePattern):
    """
    meta
    """
    def convert(self, content, props, *args, **kwargs) -> dict:
        block = super().convert(content, props, *args, **kwargs)
        m = self.pattern.match(content)
        if m:
            block["data"] = m.group("data")
            for p in self.props:
                if p == "data":
                    continue
                block["props"].update({p: m.group(p)})
            
        return block