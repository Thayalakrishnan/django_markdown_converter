from django_markdown_converter.helpers.utility import ReadSourceFromFile, timer
from django_markdown_converter.helpers.processors import process_input_content
from django_markdown_converter.patterns.classes.base import BasePattern
#from django_markdown_converter.convert import Tokenize

import time, json, gc
from functools import wraps

import re

class CustomScanner(re.Scanner):
    
    def scan(self, string:str=""):
        match = self.scanner.scanner(string).match
        i = 0
        counter = 0
        while True:
            m = match()
            if not m:
                break 
            j = m.end()
            if i == j:
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                self.match = m
                token, value, is_block  = action(m.group())
                if is_block:
                    counter+=1
                    #yield (token, value, counter)
                    yield token
                
            i = j
        #yield ["paragraph", string[i:]]
        yield "paragraph"

"""
the lambda receive the value of the token
the lambda should return, in order
label, token value, if the token can be nested
"""
class TokenizerClass:
    """
    a token is made up of a pattern and its label
    """
    PROPS_PATTERN = r'(?:^\{(?P<props>.*?)\} *?$\n)?^\n'
    
    def __init__(self) -> None:
        self.tokenizer = None
        self.tokens = []
        self.tracker = {}
        
        # adding tokens
        self.add_token(label="code", pattern=r"^```.*?^```\n")
        self.add_token(label="meta", pattern=r"^---.*?^---\n")
        self.add_token(label="attrs", pattern=r"^\{.*?\}.*?\n", is_block=False)
        
        self.add_token(label="heading", pattern=r"^\#{1,6} .*?\n", flags="m")
        self.add_token(label="olist", pattern=r"(?:^\d+\. .*?\n)(?:^(?:\d+\.)? +?.*?\n){0,}", flags="m")
        self.add_token(label="ulist", pattern=r"(?:^- .*?\n)(?:^-? +?.*?\n){0,}", flags="m")
        self.add_token(label="blockquote", pattern=r"(?:^\>.*?\n)+", flags="m")
        self.add_token(label="dlist", pattern=r"^.*?\n(?:^\: .*?\n)+", flags="m")
        self.add_token(label="admonition", pattern=r"^\!{3}.*?\n(?: {4}.*?\n)+", flags="m")
        self.add_token(label="hr", pattern=r"^[\-\*]{3}\n", flags="m")
        self.add_token(label="table", pattern=r"(?:^\|.*?\|$\n)+", flags="m")
        
        self.add_token(label="footnote", pattern=r"(?:\[\^\d+\]\:\n)(?:^ +?.*?\n)+", flags="m")
        self.add_token(label="image", pattern=r"^\!\[.*?\]\(.*?\)\n", flags="m")
        
        self.add_token(label="html", pattern=r"\<(\S+)[^\>\<]*?\>.*?\<\/\1\>")
        self.add_token(label="svg", pattern=r"<svg[^\>\<]*?\>.*?\<\/svg\>")
        
        self.add_token(label="emptyline", pattern=r"^\n", is_block=False)
        self.add_token(label="newline", pattern=r"\n", is_block=False)
        self.add_token(label="paragraph", pattern=r"^.+?\n")
        self.add_token(label="none", pattern=r".", is_block=False)
        
        # creating tokenizer
        self.create_tokenizer()
        
    def create_tokenizer(self):
        self.tokenizer = CustomScanner(self.tokens)
        
    def add_token(self, label="text", pattern:str=r"", flags:str="ms", is_block:bool=True):
        #token = (f"{pattern}{self.PROPS_PATTERN}", lambda value: [label, value])
        token = (f"(?{flags}:{pattern})", lambda value: [label, value, is_block])
        self.tokens.append(token)
        
    def reset_tracker(self):
        for _ in self.tracker.keys():
            self.tracker[_] = False
        
    def tokenize(self, source):
        self.reset_tracker()
        return self.tokenizer.scan(source)


PATH_TO_FILE = "notes/examples/post.md"

#@timer
def get_source(path):
    chunk = ReadSourceFromFile(path)
    return process_input_content(chunk)

def run_tokenizer(source):
    tk = TokenizerClass()
    m = tk.tokenize(source)
    for _ in m:
        yield(_)


def run_tokenizer_in_console(path):
    source = get_source(path)
    print(f"run_tokenizer_in_console: start")
    m = run_tokenizer(source)
    for _ in m:
        print(f"{_}")
    print(f"run_tokenizer_in_console: done")

#run_tokenizer_in_console(PATH_TO_FILE)

#print(f"done")