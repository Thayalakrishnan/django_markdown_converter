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
        yield ["paragraph", string[i:]]

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

class MegaTokenizerClass:
    """
    a token is made up of a pattern and its label
    """
    PROPS_PATTERN = r'(?:^\{(?P<props>.*?)\} *?$\n)?^\n'
    
    def __init__(self) -> None:
        self.tokenizer = None
        self.tokens = []
        self.not_blocks = []
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
        
    def add_token(self, label="text", pattern:str=r"", flags:str="ms", is_block:bool=True):
        token = f"(?P<{label}>(?{flags}:{pattern}))"
        if not is_block:
            self.not_blocks.append(label)
        self.tokens.append(token)
        
    def tokenize(self, source):
        matches = self.tokenizer.finditer(source)
        for match in matches:
            token = match.lastgroup
            if token not in self.not_blocks:
                yield token

    def create_tokenizer(self):
        patterns = "|".join(self.tokens)
        self.tokenizer = re.compile(patterns)

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""
PATH_TO_FILE = "notes/examples/post.md"

#@timer
def get_source(path):
    #print("processed -------------------------")
    chunk = ReadSourceFromFile(path)
    return process_input_content(chunk)


#@timer
def run_tokenizer(tokenizer_class):
    source = get_source(PATH_TO_FILE)
    tk = tokenizer_class()
    tokenizer = tk.tokenize(source)
    for new in tokenizer:
        pass
    return

def loop_tokenizer(tokenizer_class):
    for i in range(100):
        run_tokenizer(tokenizer_class)

@timer
def old_class():
    loop_tokenizer(BasePattern)

@timer
def new_class():
    loop_tokenizer(TokenizerClass)


@timer
def mega_class():
    loop_tokenizer(MegaTokenizerClass)


def loop_loop_tokenizer():
    funcies = [
        mega_class,
        new_class,
        old_class,
    ]
    while len(funcies):
        current = funcies.pop()
        for i in range(5):
            current()
            gc.collect()
        gc.collect()
        
    #for i in range(5):
    #    old_class()
    #    gc.collect()
    #gc.collect()
    #
    #for i in range(5):
    #    mega_class()
    #    gc.collect()
    #gc.collect()
    #print(gc.get_stats())


loop_loop_tokenizer()


##@timer
#def run_mega_tokenizer():
#    source = get_source(PATH_TO_FILE)
#    tk = TokenizerClass()
#    tk.mega_tokenize(source)
#    return
#
#run_mega_tokenizer()


#@timer
def compare_tokenizer():
    source = get_source(PATH_TO_FILE)
    
    mtk = MegaTokenizerClass()
    mtktokenizer = mtk.tokenize(source)
    
    tk = TokenizerClass()
    tktokenizer = mtk.tokenize(source)
    
    for m,t in zip(mtktokenizer,tktokenizer):
        if m != t:
            print(f"mega: {m} | scanner: {t}")        
    return


#compare_tokenizer()
print(f"done")        