#%%
import random
from faker import Faker
from typing import Callable

fake = Faker()

INDENT = "    "
WEIGHTED_CHOICE = [1]*10 + [2]*8 + [3]*4 + [4]*2

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)

SCAFFOLD_JOINLINES = lambda x=[]: "\n".join(x)
SCAFFOLD_FENCED = lambda o="", x=[],c="": "\n".join([o, *x, c, ""])
SCAFFOLD_META = lambda x=[]: SCAFFOLD_FENCED("---", x,"---")
SCAFFOLD_ATTRS = lambda x: LAM_SPACED_JOIN(["{", x,"}"])

LAM_HTML_TAG = lambda x,b: f"<{x}>{b}</{x}>"
LAM_RANDOM_INT = lambda l,u: random.randint(l,u)
LAM_RANDOM_RANGE = lambda l,u: range(LAM_RANDOM_INT(l,u))
LAM_INDENT_LINES = lambda c="": [INDENT + _ for _ in c.splitlines()]

LAMGEN_FAKE_WORDS = lambda l=1,u=5: LAM_SPACED_JOIN(fake.words(nb=LAM_RANDOM_INT(l,u)))
LAMGEN_DECISION = lambda w=50: random.randint(1,100) < w

class State:
    INLINE_MARKUP_LIST = [
        ("`", "`",),
        ("``", "``",),
        ("**", "**",),
        ("_", "_",),
        (":", ":",),
        ("^", "^",),
        ("~", "~",),
        ("$", "$",),
        ("<", ">",),
        ("--", "--",),
        ("==", "==",),
    ]
    SENTENCE_ENDINGS = ["."]*10 + ["!"]*3 + ["?"]*2 + [";"]*1
    def __init__(self):
        self.heading_level = 2
        self.footnote_index = 1
        self.footnote_count = 0
        self.inline_markup_count = 0
        self.current_depth = 0

def generate_list_item(listtype:str="ulist", level:int=0, counter:int=1, content:str=""):
    indent = level*' '*4
    delimter = "- " if listtype == "ulist" else f"{counter}. "
    if not content:
        content = LAMGEN_FAKE_WORDS(1,6).capitalize()

    return f"{indent}{delimter}{content}"

def generate_list_block(listtype="", num_items:int=1, counter:int=1, indentation_level:int=0):
    items = []
    for item in range(num_items):
        items.append(generate_list_item(listtype, indentation_level, counter))
        counter+=1
    return items

def generate_list(state:State=None, listtype=""):
    items = []
    stack = []
    indent_counter = 0
    num_list_blocks = random.randint(1,5)

    # initial item
    current_counter = 1
    items.append(generate_list_item(listtype, indent_counter, current_counter))
    current_counter+=1

    for item in range(num_list_blocks):
        num_list_items = random.randint(1,3)

        if LAMGEN_DECISION():
            # indent
            indent_counter+=1
            stack.append(current_counter)
            current_counter = 1
        else:
            # outdent
            if indent_counter:
                indent_counter-=1
                current_counter = stack.pop()

        items.extend(generate_list_block(
            listtype=listtype,
            num_items=num_list_items,
            counter=current_counter,
            indentation_level=indent_counter
        ))
        current_counter+=num_list_items

    # decide to close list or not
    if LAMGEN_DECISION():
        while len(stack):
            indent_counter-=1
            current_counter = stack.pop()
            items.append(generate_list_item(listtype, indent_counter, current_counter))
    return SCAFFOLD_JOINLINES(items)

def indent_content(content:str="") -> str:
    return "\n".join([INDENT + _ for _ in content.split("\n")])

def generate_sub_content(state:State=None, is_indented:bool=False, content_type:str="blocks" ):
    """
    return words, sentences, text only content or other blocks
    content_type: words, sentence, sentences, blocks
    """
    print("[generate_sub_content]")
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
    if is_indented:
        return indent_content(content)
    return content


def join_table_row(row):
    return f"| {' | '.join(row)} |"

def generate_table_row(size:int=0):
    row = [LAMGEN_FAKE_WORDS(1,3) for _ in range(size)]
    return join_table_row(row)

def adjust_heading_level(lvl:int=2) -> int:
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
    inline_markup = state.INLINE_MARKUP_LIST

    for w in range(sentence_length):
        word = fake.word()

        if LAMGEN_DECISION(10):
            state.inline_markup_count+=1
            imarkup = random.choice(inline_markup)
            if imarkup not in stack:
                stack.append(imarkup)
                word = imarkup[0] + word

        # close_inline_markup
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
    return " ".join(words)


def generate_sentences(state:State=None, has_inline_markup:bool=True):
    sentences = [generate_sentence(state, has_inline_markup) for _ in LAM_RANDOM_RANGE(1,6)]
    return LAM_SPACED_JOIN(sentences)


######################
def generate_attributes(state:State=None):
    pairs = [f"{fake.word()}=\"{LAMGEN_FAKE_WORDS(1,5)}\"" for _ in LAM_RANDOM_RANGE(1,5)]
    joined = LAM_SPACED_JOIN(pairs)
    return SCAFFOLD_ATTRS(joined)

def generate_meta(state:State=None):
    """
    generate the key value pairs
    - generate random number of lines
    - might have types later, but for now just single word paired
    with some ofther words
    """
    pairs = [f"{fake.word()}: {LAMGEN_FAKE_WORDS()}" for _ in LAM_RANDOM_RANGE(1,5)]
    return SCAFFOLD_META(pairs)

def generate_code(state:State=None):
    """
    language: random
    content: lines of sentences
    """
    lines = []
    header = ["```"]
    if LAMGEN_DECISION(80):
        language = random.choice(["python", "javascript", "c", "cpp", "assembly", "css", "html"])
        header.append(language)

    lines.append(LAM_JOIN("", header))

    # blocks
    for _ in LAM_RANDOM_RANGE(1,5):
        # lines
        for _ in LAM_RANDOM_RANGE(1,5):
            lines.append(LAMGEN_FAKE_WORDS(2, 10))
        lines.append("\n")
    lines.append("```")
    return SCAFFOLD_JOINLINES(lines)


def generate_dlist(state:State=None):
    """
    term: random word or words
    definition: words, sentences, blocks, inline markup
    """
    lines = []
    lines.append(fake.word().capitalize()) # term
    has_inline_markup = LAMGEN_DECISION(50)
    definition = [f": {generate_sentence(state, has_inline_markup)}" for _ in LAM_RANDOM_RANGE(1,3)]
    lines.extend(definition)
    return SCAFFOLD_JOINLINES(lines)


def generate_footnote(state:State=None):
    """
    index: random number
    content: words, sentences, blocks
    """
    print("[generate_footnote] Start")
    lines = []

    index = f"[^{state.footnote_index}]:"
    state.footnote_index+=1

    content = generate_sub_content(state, is_indented=True)

    lines.append(index)
    lines.append(content)

    print("[generate_footnote] Done")
    return SCAFFOLD_JOINLINES(lines)


def generate_admonition(state:State=None):
    """
    type: choice
    title: words
    content: words, sentences, blocks
    """
    print("[generate_admonition] Start")
    lines = []
    header = ["!!!"]
    if LAMGEN_DECISION(80):
        ad_type = random.choice(["note", "info", "warning", "tip", "danger", "example"])
        header.append(ad_type)
    if LAMGEN_DECISION(80):
        header.append(f'\"{LAMGEN_FAKE_WORDS(1,3)}\"')

    lines.append(LAM_SPACED_JOIN(header))
    content = generate_sub_content(state, is_indented=True)
    lines.append(content)
    print("[generate_admonition] Done")
    return SCAFFOLD_JOINLINES(lines)


def generate_table(state:State=None):
    """
    header: random number of columns
    body: random number of rows and use columns
    - cells: inline markup
    """
    lines = []
    cols = LAM_RANDOM_INT(1,10)
    rows = LAM_RANDOM_INT(1,5)

    header = generate_table_row(cols)
    lines.append(header)

    breaker = join_table_row(["---"]*cols)
    lines.append(breaker)

    for i in range(rows):
        lines.append(generate_table_row(cols))
    return SCAFFOLD_JOINLINES(lines)

def generate_hr(state:State=None):
    if LAMGEN_DECISION(80):
        return "***"
    return "---"

def generate_heading(state:State=None):
    """
    level: integer
    content: words, inline markup
    """
    level = "#"*state.heading_level
    state.heading_level = adjust_heading_level(state.heading_level)
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return f"{level} {content}"

def generate_image(state:State=None):
    """
    alt: words
    title: words
    src: url
    """
    alt = LAMGEN_FAKE_WORDS(3,10)
    title = LAMGEN_FAKE_WORDS(3,8)
    src = fake.image_url()
    return f"![{alt}]({src} \"{title}\")"

def generate_svg(state:State=None):
    """
    content: xml
    """
    content = LAMGEN_FAKE_WORDS(5,10)
    return LAM_HTML_TAG("svg", content)

def generate_html(state:State=None):
    """
    tag: word
    content: xml
    """
    tag = fake.word()
    content = LAMGEN_FAKE_WORDS(5,10)
    return LAM_HTML_TAG(tag, content)

def generate_ulist(state:State=None):
    """
    content: list item: words, sentences, blocks
    """
    return generate_list(state, "ulist")

def generate_olist(state:State=None):
    """
    content: list item: words, sentences, blocks
    """
    return generate_list(state, "olist")

def generate_blockquote(state:State=None):
    """
    content: words, sentences, blocks
    """
    content = generate_sub_content(state, is_indented=False)
    #lines = ["> " + LAMGEN_FAKE_WORDS(5,10) for _ in LAM_RANDOM_RANGE(1,5)]
    lines = ["> " + line for line in content.split("\n")]
    return SCAFFOLD_JOINLINES(lines)

def generate_paragraph(state:State=None):
    """
    content: sentences
    """
    sentences = generate_sentences(state)
    return sentences

def generate_emptyline(state:State=None):
    return "\n\n"

def generate_newline(state:State=None):
    return "\n"

def generate_none(state:State=None):
    return ""

##################################
"""
Generators
"""

def create_generators():
    generators = [
        (generate_heading, 15),
        (generate_paragraph, 15),
        (generate_ulist, 10),
        (generate_olist, 10),

        (generate_image, 8),
        (generate_code, 8),
        (generate_footnote, 5),
        (generate_admonition, 5),

        (generate_table, 3),
        (generate_svg, 2),
        (generate_html, 2),
        (generate_blockquote, 1),
        (generate_dlist, 1),
        (generate_hr, 1),
    ]
    ret = []
    for func, times in generators:
        ret+=[func]*times
    return ret

def create_nested_generators():
    generators = [
        (generate_code, 1),
        (generate_dlist, 1),
        (generate_footnote, 1),
        (generate_admonition, 1),
        (generate_table, 1),
        (generate_hr, 1),
        (generate_heading, 1),
        (generate_image, 1),
        (generate_svg, 1),
        (generate_html, 1),
        (generate_ulist, 1),
        (generate_olist, 1),
        (generate_blockquote, 1),
        (generate_paragraph, 1),
    ]
    ret = []
    for func, times in generators:
        ret+=[func]*times
    return ret


def return_markdown_blocks_list(state:State=None, generator_funcs:Callable=lambda: None, num_blocks:int=1) -> list:
    blocks = []
    for _ in range(num_blocks):
        block = random.choice(generator_funcs)(state)
        #blocks.append(block)
        
        has_attrs = LAMGEN_DECISION(30)
        if has_attrs:
            attrs = generate_attributes(state)
            #blocks.append(attrs)
            block = block + "\n" + attrs
            
        blocks.append(block)   
    return blocks

def generate_markdown_blocks(state:State=None, num_blocks:int=1, is_nested:bool=False, has_meta:bool=True):
    generator_funcs = create_generators() if not is_nested else create_nested_generators()
    blocks = []
    if has_meta and not is_nested:
        blocks.append(generate_meta(state))
    
    blocks.extend(return_markdown_blocks_list(state, generator_funcs, num_blocks))
    return "\n\n".join(blocks)




##################################
"""
Runners
generate_footnote
generate_admonition
"""
def run_generators():
    current_state = State()
    generators_list = create_generators()
    for _ in generators_list:
        name = _.__name__.split("_")[1]
        print(f"## {name}\n")
        print(_(current_state))
        print("\n")

def run_generator():
    current_state = State()
    for i in range(20):
        print(generate_blockquote(current_state))
        print("\n")

def run_get_sentences():
    current_state = State()
    num_loops = 5
    for i in range(num_loops):
        print(generate_sentence(current_state))

def run_generate_markdown_blocks():
    current_state = State()
    for i in range(5):
        num_blocks = random.randint(3,20)
        print(generate_markdown_blocks(current_state, num_blocks))

#run_generate_markdown_blocks()
run_generator()
#run_get_sentences()
#run_generators()
#%%
