from django_markdown_converter.helpers.utility import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content
import re


class CustomScanner(re.Scanner):
    
    def scan(self, string:str=""):
        match = self.scanner.scanner(string).match
        i = 0
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
                ret  = action(m.group())
                if ret[0] == "heading":
                    print(f"match: {ret[0]} | {ret[1].strip()}")
                else:
                    print(f"match: {ret[0]}")
                yield ret
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
        #self.add_token(label="code", pattern=r"```.*?```.*?")
        #self.add_token(label="meta", pattern=r"(?:\-\-\-)")
        #self.add_token(label="olist", pattern=r"(?:- .*?)")
        #self.add_token(label="ulist", pattern=r"(?:1. .*?)")
        #self.add_token(label="table", pattern=r"(?:\| .*?)")
        #self.add_token(label="blockquote", pattern=r"(?:\> .*?)")
        #self.add_token(label="dlist", pattern=r"(?:\: .*?)")
        #self.add_token(label="admonition", pattern=r"(?:\!\!\! .*?)")
        #self.add_token(label="hr", pattern=r"(?:\-\-\- *?)")
        #self.add_token(label="heading", pattern=r"(?:\#{0,6} .*?)")
        #self.add_token(label="footnote", pattern=r"(?:\[\^\d+\]\:)")
        #self.add_token(label="image", pattern=r"(?:\[.*?\]\([^ ]+?\))")
        #self.add_token(label="paragraph", pattern=r".+?")
        
        self.add_token(label="code", pattern=r"^```.*?^```\n")
        self.add_token(label="meta", pattern=r"^---.*?^---\n")
        self.add_token(label="attrs", pattern=r"^\{.*?\}.*?\n")
        
        # (?:- .*?(?=\n^\n))
        # ((?:^ *?- .*?\n)|(?:^ +?.*?\n))+
        # (?:^(?:(?: *?- )|(?: +?)).*?\n)+
        self.add_token(label="heading", pattern=r"\#{1,6} .*?\n", flags="m")
        self.add_token(label="olist", pattern=r"(?:^1.*?\n)(?:^(?:(?: *?\d+. )|(?: +?)).*?\n)+", flags="m")
        self.add_token(label="ulist", pattern=r"(?:^- .*?\n)(?:^(?:(?: *?- )|(?: +?)).*?\n)+", flags="m")
        self.add_token(label="blockquote", pattern=r"^(?:\>.*?\n)+")
        #self.add_token(label="dlist", pattern=r"\: ")
        self.add_token(label="admonition", pattern=r"^\!{3}.*?\n(?: {4}.*?\n)+", flags="m")
        self.add_token(label="hr", pattern=r"^\-{3}\n", flags="m")
        self.add_token(label="hr", pattern=r"^\*{3}\n", flags="m")
        #self.add_token(label="table", pattern=r"\|.*?\|")
        #self.add_token(label="footnote", pattern=r"\[\^\d+\]\:")
        #self.add_token(label="image", pattern=r"\[.*?\]\([^ ]+?\)")
        #self.add_token(label="misc", pattern=r".+?")
        
        #self.add_token(label="between", pattern=r"^\n")
        
        #pattern=r"(?ms:^```.*?^```\n)"
        #pattern=r"(?ms)^```.*?^```\n"
        #pattern=r"^```.*?"
        
        #self.add_token(
        #    label="code", 
        #    pattern=r"^```.*?"
        #    #pattern=r"(?s)^```.*?^```\n"
        #)
        
        
        self.add_token(label="newline", pattern=r"\n")
        self.add_token(label="paragraph", pattern=r"^.+?\n")
        #self.add_token(label="word", pattern=r"\S+")
        #self.add_token(label="whitespace", pattern=r"\s+")
        
        #self.add_token(label="html", pattern=r"(?:\<(\S+)[^\>\<]*?\>.*?\<\/\1\>)")
        #self.add_token(label="paragraph", pattern=r"(?:\~\~)|(?:\-\-)")
        #self.add_token(label="svg", pattern=r"[a-zA-Z0-9]+")
        
        # creating tokenizer
        self.create_tokenizer()
        
    def create_tokenizer(self):
        self.tokenizer = CustomScanner(self.tokens)
        
    def add_token(self, label="text", pattern:str=r"", flags:str="ms"):
        #token = (f"{pattern}{self.PROPS_PATTERN}", lambda value: [label, value])
        token = (f"(?{flags}:{pattern})", lambda value: [label, value])
        self.tokens.append(token)
        
    def reset_tracker(self):
        for _ in self.tracker.keys():
            self.tracker[_] = False
        
    def tokenize(self, source):
        self.reset_tracker()
        return self.tokenizer.scan(source)



"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""
root = []
json_root = []
json_root_nu = []
path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)

print("processed -------------------------")


#raw_chunk = """
#
#```python
#
#here is some code 
#
#```
#
#"""

raw_chunk = process_input_content(raw_chunk)

tk = TokenizerClass()
tokens = tk.tokenize(raw_chunk)

for _ in tokens:
    #print(_[0])
    pass
