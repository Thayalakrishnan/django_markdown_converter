from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import STANDARD_TYPES
from pygments.util import ClassNotFound

from django_markdown_converter.patterns.classes.base import BasePattern


def lex_format(tokensource):
    current_line = []
    lines = []
    for ttype, value in tokensource:
        if value == "\n":
            lines.append(current_line)
            current_line = []
            continue
        
        if value == " ":
            token = "w"
            current_token = (token, value)
        else:
            token = STANDARD_TYPES.get(ttype, "")
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


class CodePattern(BasePattern):
    """
    code
    """
    def get_data(self) -> dict:
        code = self.match.group("data").strip()
        language = self.match.group("language")
        if language:
            return format_code(code, language.strip())
        return format_code(code)
    
