#%%
import random
from faker import Faker
from typing import Callable

fake = Faker()

INDENT = "    "
WEIGHTED_CHOICE = [1]*10 + [2]*8 + [3]*4 + [4]*2

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)

LAM_RANDOM_INT = lambda l,u: random.randint(l,u)
LAM_RANDOM_RANGE = lambda l,u: range(LAM_RANDOM_INT(l,u))

LAMGEN_FAKE_WORDS = lambda l=1,u=5: LAM_SPACED_JOIN(fake.words(nb=LAM_RANDOM_INT(l,u)))
LAMGEN_DECISION = lambda w=50: random.randint(1,100) < w

LAM_CLAMP = lambda l,u,x: max(min(x, u), l)
LAM_CLAMP_HEADING = lambda x: LAM_CLAMP(2,6,x)
LAM_CLAMP_LIST_INDENTATION = lambda x: LAM_CLAMP(0,4,x)
LAM_LIST_INDENT_UNDENT = lambda x: x + random.choice([-1, 0, 1])
LAM_ADJUST_LIST_INDENTATION = lambda x: LAM_CLAMP(0,4,LAM_LIST_INDENT_UNDENT(x))

class State:
    INLINE_MARKUP_LIST = [("`", "`",),("``", "``",),("**", "**",),("_", "_",),(":", ":",),("^", "^",),("~", "~",),("$", "$",),("<", ">",),("--", "--",),("==", "==",),]
    SENTENCE_ENDINGS = ["."]*10 + ["!"]*3 + ["?"]*2 + [";"]*1
    def __init__(self):
        self.heading_level = 2
        self.footnote_index = 1
        self.footnote_count = 0
        self.inline_markup_count = 0
        self.current_depth = 0

def generate_list_item(list_type:str="u", ctr:int=1, ind:int=0) -> tuple:
    indent = ind*4
    delimter = "-" if list_type == "u" else ctr
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return indent, delimter, content

def generate_list_loop(items:list=[], current:list=[], stack:list=[]):
    """stack: type, ctr, ind"""
    items.append(generate_list_item(*current))
    new_ind = LAM_ADJUST_LIST_INDENTATION(current[2])
    current[1] += 1
    
    # indent
    if new_ind > current[2]:
        stack.append(current)
        return items, [current[0], 1, current[2]+1], stack
    # unindent
    elif new_ind < current[2]:
        return items, stack.pop(), stack
    # stay the same
    return items, current, stack

def generate_list(state:State=None, list_type=""):
    items, stack, current  = [], [], [list_type, 1, 0]
    max_items = random.randint(1,20)
    
    while len(items) < max_items:
        items, current, stack = generate_list_loop(items, current, stack)
    return items

def generate_sub_content(state:State=None, is_indented:bool=False, content_type:str="blocks" ):
    """
    return words, sentences, text only content or other blocks
    content_type: words, sentence, sentences, blocks
    """
    # if nested depth is too deep, we can return just sentences
    state.current_depth+=1
    if state.current_depth > 3:
        content = LAMGEN_FAKE_WORDS(1,5)
    # return words
    elif LAMGEN_DECISION() or content_type=="words":
        content = LAMGEN_FAKE_WORDS(1,5)
    # reutrn sentence
    elif LAMGEN_DECISION() or content_type=="sentence":
        content = generate_sentence(state, LAMGEN_DECISION())
    # return sentences
    elif LAMGEN_DECISION() or content_type=="sentences":
        content = generate_sentences(state, LAMGEN_DECISION())
    else:
        # return blocks
        num_blocks = LAM_RANDOM_INT(1,5)
        content = generate_markdown_blocks(state, num_blocks=num_blocks, is_nested=False, has_meta=False)
    state.current_depth-=1
    return content


def generate_table_row(size:int=0):
    row = [LAMGEN_FAKE_WORDS(1,3) for _ in range(size)]
    return row

def adjust_heading_level(lvl:int=2) -> int:
    """shift the heading level up or down one or leave unchanged"""
    new_lvl = lvl + random.choice([-1, 0, 0, 1, 1])
    if new_lvl < 2:
        return 2
    if new_lvl > 6:
        return 6
    return new_lvl

"""
## not
"footnote": lambda x: f"[^{x}]",
"link": lambda x: f"{x.get('title', '')}]({x.get('to', '')}",
"""
def generate_plain_sentence(state:State=None, sentence_length:int=1):
    return [fake.word() for w in range(sentence_length)]

def generate_markedup_sentence(state:State=None, sentence_length:int=1):
    stack = []
    words = []
    inline_markup_list = state.INLINE_MARKUP_LIST

    for w in range(sentence_length):
        word = fake.word()

        if LAMGEN_DECISION(10):
            state.inline_markup_list_count+=1
            imarkup = random.choice(inline_markup_list)
            if imarkup not in stack:
                stack.append(imarkup)
                word = imarkup[0] + word

        # close_inline_markup_list
        if len(stack) and LAMGEN_DECISION(90):
            imarkup = stack.pop()
            word = word + imarkup[1]

        words.append(word)

    while len(stack):
        imarkup = stack.pop()
        words[-1]+=imarkup[1]
    return words


def generate_sentence(state:State=None, has_inline_markup:bool=True):
    sentence_length = random.randint(5,20)
    words = generate_markedup_sentence(state, sentence_length) if has_inline_markup else generate_markedup_sentence(state, sentence_length)
    ending = random.choice(state.SENTENCE_ENDINGS)
    words[-1]+=ending
    words[0] = words[0].capitalize()
    return " ".join(words)

def generate_sentences(state:State=None, has_inline_markup:bool=True):
    sentences = [generate_sentence(state, has_inline_markup) for _ in LAM_RANDOM_RANGE(1,6)]
    return LAM_SPACED_JOIN(sentences)

##################################
"""
Block Generators
content
"""

def generate_attributes(state:State=None):
    pairs = [(fake.word(), LAMGEN_FAKE_WORDS()) for _ in LAM_RANDOM_RANGE(1,5)]
    return (pairs)

def generate_meta(state:State=None):
    """
    generate the key value pairs
    - generate random number of lines
    - might have types later, but for now just single word paired
    with some ofther words
    """
    pairs = [(fake.word(), LAMGEN_FAKE_WORDS()) for _ in LAM_RANDOM_RANGE(1,5)]
    return (("pairs", pairs))

def generate_code(state:State=None):
    """
    language: random
    content: lines of sentences
    """
    content = []
    languages = ["python", "javascript", "c", "cpp", "assembly", "css", "html"]
    language = random.choice(languages) if LAMGEN_DECISION(80) else ""
    # blocks
    for _ in LAM_RANDOM_RANGE(1,5):
        # lines
        for _ in LAM_RANDOM_RANGE(1,5):
            content.append(LAMGEN_FAKE_WORDS(2, 10))
        content.append("\n")
    return (("language", language), ("content", content))


def generate_dlist(state:State=None):
    """
    term: random word or words
    definition: words, sentences, blocks, inline markup
    """
    term = fake.word().capitalize()
    has_inline_markup = LAMGEN_DECISION(50)
    definition = [generate_sentence(state, has_inline_markup) for _ in LAM_RANDOM_RANGE(1,3)]
    return (("term", term), ("definition", definition))


def generate_footnote(state:State=None):
    """
    index: random number
    content: words, sentences, blocks
    """
    index = state.footnote_index
    state.footnote_index+=1
    content = generate_sub_content(state, is_indented=True)
    return (("index", index), ("content", content))


def generate_admonition(state:State=None):
    """
    type: choice
    title: words
    content: words, sentences, blocks
    """
    ad_type_choices = ["note", "info", "warning", "tip", "danger", "example"]
    
    ad_type = random.choice(ad_type_choices) if LAMGEN_DECISION(80) else ""
    ad_title = LAMGEN_FAKE_WORDS(1,3) if LAMGEN_DECISION(80) else ""
    content = generate_sub_content(state, is_indented=True)
    return (("type", ad_type), ("title", ad_title), ("content", content))


def generate_table(state:State=None):
    """
    header: random number of columns
    body: random number of rows and use columns
    - cells: inline markup
    """
    cols = LAM_RANDOM_INT(1,10)
    rows = LAM_RANDOM_INT(1,5)

    header = generate_table_row(cols)
    breaker = ["---"]*cols
    body = [generate_table_row(cols) for i in range(rows)]
    return (("header", header), ("breaker", breaker), ("body", body))

def generate_hr(state:State=None):
    content = "***" if LAMGEN_DECISION(80) else "---"
    return (("content", content))

def generate_heading(state:State=None, level:int=0):
    """
    level: integer
    content: words, inline markup
    """
    level = state.heading_level if not level else level
    if not level:
        state.heading_level = adjust_heading_level(state.heading_level)
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return (("level", level), ("content", content))

def generate_image(state:State=None):
    """
    alt: words
    title: words
    src: url
    """
    alt = LAMGEN_FAKE_WORDS(3,10)
    title = LAMGEN_FAKE_WORDS(3,8)
    src = fake.image_url()
    return (("alt", alt), ("title", title), ("src", src))

def generate_svg(state:State=None):
    """
    content: xml
    """
    content = LAMGEN_FAKE_WORDS(5,10)
    return (("content", content))

def generate_html(state:State=None):
    """
    ret: tag -> word
    ret: content -> xml
    """
    tag = fake.word()
    content = LAMGEN_FAKE_WORDS(5,10)
    return (("content", content), ("tag", tag))

def generate_ulist(state:State=None):
    """
    content: list item: words, sentences, blocks
    """
    return (("items", generate_list(state, "u")))


def generate_olist(state:State=None):
    """
    content: list item: words, sentences, blocks
    """
    return (("items", generate_list(state, "o")))


def generate_blockquote(state:State=None):
    """
    ret: content -> words, sentences, blocks
    """
    content = generate_sub_content(state, is_indented=False)
    return (("content", content))

def generate_paragraph(state:State=None):
    """
    ret: content -> words, sentences, blocks
    """
    content = generate_sentences(state)
    return (("content", content))

def generate_emptyline(state:State=None):
    return (("content", "\n\n"))

def generate_newline(state:State=None):
    return (("content", "\n"))

def generate_none(state:State=None):
    return (("content", ""))

##################################
"""
Generators
structure: 
name, content, attributes
"""

def create_generators(weighted:bool=True):
    generators = [
        (generate_heading, 30),
        (generate_paragraph, 30),
        (generate_ulist, 20),
        (generate_olist, 20),

        (generate_image, 10),
        (generate_code, 10),
        (generate_footnote, 8),
        (generate_admonition, 8),

        (generate_table, 3),
        (generate_svg, 2),
        (generate_html, 2),
        (generate_blockquote, 1),
        (generate_dlist, 1),
        (generate_hr, 1),
    ]
    if weighted:
        return [f for func,weight in generators for f in [func]*weight]
    return [func for func,weight in generators]

LAM_FUNC_NAMNE = lambda func: func.__name__.split("_")[1]


def generate_markdown_blocks(state:State=None, num_blocks:int=1, is_nested:bool=False, has_meta:bool=True):
    generator_funcs = create_generators(weighted=True)
    blocks = []
    
    if has_meta and not is_nested:
        blocks.append((LAM_FUNC_NAMNE(generate_meta), generate_meta(state), None))
        
    for _ in range(num_blocks):
        gen_func = random.choice(generator_funcs)
        
        name = LAM_FUNC_NAMNE(gen_func)
        block = gen_func(state)
        attrs = generate_attributes(state) if LAMGEN_DECISION(30) else None
        
        blocks.append((name, block, attrs))
        
    return blocks

##################################
"""
Runners
generate_footnote
generate_admonition
"""

def run_generators():
    current_state = State()
    generators_list = create_generators(weighted=False)
    for gen_func in generators_list:
        name = LAM_FUNC_NAMNE(gen_func)
        block = gen_func(current_state)
        attrs = generate_attributes(current_state) if LAMGEN_DECISION(30) else None
        
        print(f"## {name}")
        print((name, block, attrs))
        print("\n")
        
def run_generate_markdown_blocks():
    current_state = State()
    generators_list = create_generators(weighted=False)
    blocks = generate_markdown_blocks(current_state, 5, False, False)
    for b in blocks:
        print(b)
        
def run_generator():
    current_state = State()
    for b in range(5):
        print(generate_paragraph(current_state))

run_generator()
#run_generators()
#run_generate_markdown_blocks()


#%%
