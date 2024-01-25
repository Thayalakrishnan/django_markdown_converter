import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from blockifiers.base_blockifier import BaseBlockifier

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

class CodeBlockifier(BaseBlockifier):
    """ Process code blocks. """
    __slots__ = ("custom_formatter",)
    
    def setUp(self, *args, **kwargs) -> None:
        self.custom_formatter = CustomFormatter(**PYG_CONFIG)
    
    def getData(self, match, props, *args, **kwargs):
        if match.group('content'):
            content = match.group('content')
            lexer = get_lexer_by_name(props['language'], **PYG_CONFIG)
            return highlight(content, lexer, self.custom_formatter)
        return ""

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt
