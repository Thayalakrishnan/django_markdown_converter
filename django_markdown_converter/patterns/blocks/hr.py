from django_markdown_converter.patterns.classes.base import BasePattern


class HRPattern(BasePattern):
    pass

    def revert(self, *args, **kwargs) -> str:
        block = super().revert(*args, **kwargs)
        data = block.get("data", "---")
        ret = []
        ret.append(data)
        ret.append("")
        return "\n".join(ret)