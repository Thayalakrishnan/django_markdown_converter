#%%
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import STANDARD_TYPES
from pygments.util import ClassNotFound


def lex_format(tokensource):
    print(tokensource)
    current_line = []
    lines = []
    for ttype, value in tokensource:
        print(ttype)
        print(value)
        if value == "\n":
            lines.append(current_line)
            current_line = []
            continue
        
        if value == " ":
            token = "w"
            current_token = (token, value)
        else:
            token = STANDARD_TYPES[ttype]
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
    

source = """# test code
for i in range(5):
    print(i)
"""
    
formatted_code = format_code(source, "")
for _ in formatted_code:
    print(_)

print("done")



# %%
