from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import STANDARD_TYPES
from pygments.util import ClassNotFound

from django_markdown_converter.patterns.classes.base import Pattern
from django_markdown_converter.patterns.data import CODE_PATTERN



def lex_format(tokensource):
    current_line = []
    lines = []
    for ttype, value in tokensource:
        
        if value == "\n":
            lines.append(current_line)
            current_line = []
            continue
        
        token = STANDARD_TYPES.get(ttype, "")
        if not token and " " in value:
            token = "w"
            current_token = (token, value)
        
        current_token = (token, value)
        current_line.append(current_token)
    
    if not len(lines):
        lines.append(current_line)
    return lines


def format_code(source:str="", language:str=""):
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        # if not class found, we need 
        # to manually process the code into lines
        source = source.strip("\n")
        tokensource = [('text', _) for _ in source.split("\n")]
        return tokensource
    
    # lex returns a token iterator
    # that we can loop over
    lex_ret = lex(source, lexer)
    return lex_format(lex_ret)


class CodePattern(Pattern):
    """
    code
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="code", pattern_object=CODE_PATTERN, *args, **kwargs)
            
    def get_data(self) -> dict:
        code = self.match.group("data").strip()
        language = self.match.group("language")
        if language:
            return format_code(code, language.strip())
        return format_code(code)
    

    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        
        props = self.block.get("props", {})
        language = props.get("language", '')
        
        middle = []
        data = self.block.get("data", "")
        for row in data:
            line = "".join(list(map(lambda x: x[1], row)))
            middle.append(line)
    
        ret = []
        ret.append(f"```{language}")
        ret.extend(middle)
        ret.append(f"```")
        ret.append("")
        return "\n".join(ret)