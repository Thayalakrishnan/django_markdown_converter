import re
from notes.tools import get_source

def buffered_generator(generator):
    current_value = next(generator)
    while True:
        try:
            next_value = next(generator)
            yield current_value
            current_value = next_value
        except StopIteration:
            yield current_value
            break
    yield False, False

class MegaTokenizerClass:
    """
    a token is made up of a pattern and its label
    """
    
    def __init__(self) -> None:
        self.tokenizer = None
        self.tokens = []
        self.not_blocks = []
        self.blocks = []
        self.tracker = {}
        
        # adding tokens
        self.add_token(label="code", pattern=r"^```.*?^```\n")
        self.add_token(label="meta", pattern=r"^---.*?^---\n")
        #self.add_token(label="attrs", pattern=r"^\{.*?\}.*?\n", is_block=False)
        self.add_token(label="attrs", pattern=r"^\{.*?\}.*?\n")
        
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
        patterns = "|".join(self.tokens)
        self.tokenizer = re.compile(patterns)
        
    def add_token(self, label="text", pattern:str=r"", flags:str="ms", is_block:bool=True):
        token = f"(?P<{label}>(?{flags}:{pattern}))"
        if is_block:
            self.blocks.append(label)
        else:
            self.not_blocks.append(label)
        self.tokens.append(token)
    
    def tokenize(self, source):
        matches = self.tokenizer.finditer(source)
        for match in matches:
            token = match.lastgroup
            value = match.group(token)
            if token not in self.not_blocks:
                yield token, value
    

PATH_TO_FILE = "notes/examples/post.md"

def lagging_generator(source):
    
    mtk = MegaTokenizerClass()
    token_generator = mtk.tokenize(source)
    
    tokens = buffered_generator(token_generator)
    current = next(tokens)
    
    while current:
        current_token, current_value = current
        
        if current_token:
            if current_token in mtk.blocks:
                nxt = next(tokens)
                nxt_token, nxt_value = nxt
                if nxt_token: 
                    if nxt_token == "attrs":
                        yield current, nxt
                        current = next(tokens)
                    else:
                        yield current, None
                        current = nxt
                else:
                    yield current, None
                    break
            else:
                current = next(tokens)
        else:
            # if current token is false, exist the looop
            break


def run_mega_tokenizer(source):
    m = lagging_generator(source)
    for _ in m:
        yield(_[0])

def run_mega_tokenizer_in_console(path):
    source = get_source(path)
    print(f"run_mega_tokenizer_in_console: start")
    m = run_mega_tokenizer(source)
    for _ in m:
        print(f"{_}")
    print(f"run_mega_tokenizer_in_console: done")


#run_mega_tokenizer_in_console(PATH_TO_FILE)