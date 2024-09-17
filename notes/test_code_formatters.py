#%%
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter
from pygments.formatters import HtmlFormatter

PYG_CONFIG = {
    'linenums': False,
    'guess_lang': False,
    'css_class': 'highlight',
    'noclasses': False,
    'use_pygments': True,
    'lang_prefix': 'language-',
    'pygments_formatter': 'html',
    'nowrap ': False,
    'linenos': False,
    'filename': 'filename',
    'linespans': 'line',
    'cssclass': 'codeblock',
    'debug_token_types': False
}

class NullFormatter(Formatter):
    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            print(f'{ttype} : {repr(value)}')
            outfile.write(value)
            #return value


class CustomFormatter(HtmlFormatter):
    
    def wrap(self, source, *args):
        return self._wrap_code(source, *args)

    def _wrap_code(self, source, *args):
        yield 0, '<code>'
        for i, t in source:
            yield i, t
        yield 0, '</code>'

    def _wrap_div(self, inner,*args):
        yield 0, ('')
        yield from inner
        yield 0, '\n'


source = """# test code
for i in range(5):
    print(i)
"""

lexer = get_lexer_by_name("python")
ret = highlight(source, lexer, NullFormatter(**PYG_CONFIG))

print(ret)
print("done")



# %%
