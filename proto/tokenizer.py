# %%
import re
from typing import Callable, Optional

class CustomScanner(re.Scanner):
    
    def scan(self, string:str="", tracker:dict={}):
        text_group = ""
        match = self.scanner.scanner(string).match
        i = 0
        while True:
            m = match()
            if not m:
                # no match, break and return string
                break
            j = m.end()
            if i == j:
                # set j to the end of the match
                # if i is equal to j, we have matched
                # at the end again so break
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                # (token, value, nestable, is open)
                self.match = m
                ret  = action(m.group())
                if ret[0] == "text":
                    text_group+=ret[1]
                else:
                    if len(text_group):
                        yield ["text", text_group, False, False]
                    text_group = ""
                    if ret[2]:
                        tracker[ret[0]] = not tracker[ret[0]]
                        ret[3] = tracker[ret[0]]
                    yield ret
            # set i to j so we know
            # we are moving along the string
            i = j
        text_group+=string[i:]
        yield ["text", text_group, False, False]


"""
the lambda receive the value of the token
the lambda should return, in order
label, token value, if the token can be nested
"""
class TokenizerClass:
    """
    a token is made up of a pattern and its label
    """
    def __init__(self) -> None:
        print(f"[proto][tokenizer][TokenizerClass][__init__]")
        
        self.tokenizer = None
        self.tokens = []
        self.tracker = {}
        
        self.add_token(label="strong", pattern=r"(?:\*\*)|(?:__)", is_nestable=True)
        self.add_token(label="del", pattern=r"(?:\~\~)|(?:\-\-)", is_nestable=True)
        self.add_token(label="mark", pattern=r"\=\=", is_nestable=True)
        self.add_token(label="sup", pattern=r"\^(?=[^\^])", is_nestable=True)
        self.add_token(label="sub", pattern=r"\~(?=[^\~])", is_nestable=True)
        self.add_token(label="em", pattern=r"(?:\*)|(?:_)", is_nestable=True)
        self.add_token(label="samp", pattern=r"``", is_nestable=True)
        self.add_token(label="code", pattern=r"`", is_nestable=True)
        self.add_token(label="math", pattern=r"\$.*?\$", is_nestable=False)
        self.add_token(label="emoji", pattern=r"\:.*?\:", is_nestable=False, modifier=lambda x: x[1:-1])
        self.add_token(label="footnote", pattern=r"\[\^\d+\]", is_nestable=False, modifier=lambda x: x[2:-1])
        self.add_token(label="link", pattern=r"\[.*?\]\([^ ]+?\)", is_nestable=False)
        self.add_token(label="html", pattern=r"\<(\S+)[^\>\<]*?\>.*?\<\/\1\>", is_nestable=False)
        self.add_token(label="rawlink", pattern=r"\<[^ ]+?\>", is_nestable=False, modifier=lambda x: x[1:-1])
        self.add_token(label="text", pattern=r"[a-zA-Z0-9]+", is_nestable=False)
        self.add_token(label="text", pattern=r"\s+", is_nestable=False)
        self.add_token(label="text", pattern=r".+?", is_nestable=False)
        print(self.tracker)
        self.create_tokenizer()
        
    def create_tokenizer(self):
        self.tokenizer = CustomScanner(self.tokens)
        
    def add_token(self, label="text", pattern:str=r"", is_nestable:bool=False, modifier:Optional[Callable]=None):
        if is_nestable:
            self.tracker[label] = False
        if modifier:
            token = (pattern, lambda value: [label, modifier(value), is_nestable, False])
        else:
            token = (pattern, lambda value: [label, value, is_nestable, False])
        self.tokens.append(token)
        
    def reset_tracker(self):
        for _ in self.tracker.keys():
            self.tracker[_] = False
        
    def tokenize(self, source):
        print(f"[proto][tokenizer][TokenizerClass][tokenize]")
        self.reset_tracker()
        return self.tokenizer.scan(source, self.tracker)


Tokenizer = TokenizerClass()
