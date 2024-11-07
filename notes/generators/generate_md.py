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

def generate_list_item(list_type:str="ulist", level:int=0, counter:int=1):
    indent = level*' '*4
    delimter = "- " if list_type == "ulist" else f"{counter}. "
    content = LAMGEN_FAKE_WORDS(1,6).capitalize()
    return f"{indent}{delimter}{content}"

def generate_list_block(list_type="", num_items:int=1, counter:int=1, indentation_level:int=0):
    return [generate_list_item(list_type, indentation_level, item) for item in range(counter, counter + num_items)]

def adjust_indentation(lvl:int=0) -> int:
    new_lvl = lvl + 1 if LAMGEN_DECISION() else lvl - 1
    return LAM_CLAMP_LIST_INDENTATION(new_lvl)

def generate_list_recursively(max_items:int=0, items:list=[], list_type:str="ulist", counter:int=1, indentation:int=1):
    print(f"indentation {indentation} ################")
    
    if len(items) > max_items:
        return items, list_type, counter, indentation
    
    num_items = random.randint(1,3)
    items.extend(generate_list_block(list_type, num_items, counter, indentation))
    
    #new_counter = counter + num_items
    new_indentation = LAM_ADJUST_LIST_INDENTATION(indentation)
    
    if new_indentation > indentation:
        generate_list_recursively(max_items, items, list_type, 1, indentation + 1)
    #elif new_indentation == indentation:
    #items, list_type, counter, indentation = generate_list_recursively(max_items, items, list_type, counter + num_items, indentation)
    #    return items, list_type, counter + num_items, indentation
    #return items, list_type, counter + num_items, indentation - 1
    if new_indentation < indentation and new_indentation > 0:
        items, list_type, counter, indentation = generate_list_recursively(max_items, items, list_type, counter, indentation - 1)
    return items, list_type, counter + num_items, indentation
    #return items, list_type, counter + num_items, indentation
        
def generate_list(state:State=None, list_type=""):
    items = []
    indentation = 0
    counter = 1
    
    for _ in LAM_RANDOM_RANGE(1,5):
        items, list_type, counter, indentation = generate_list_recursively(items, list_type, counter, indentation)
    return SCAFFOLD_JOINLINES(items)

def generate_list(state:State=None, list_type=""):
    items = []
    indentation = 0
    counter = 1
    max_items = random.randint(1,20)
    
    while len(items) < max_items:
        items, list_type, counter, indentation = generate_list_recursively(max_items, items, list_type, counter, indentation)
    return SCAFFOLD_JOINLINES(items)

def indent_content(content:str="") -> str:
    return "\n".join([INDENT + _ for _ in content.split("\n")])

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
    return LAM_CLAMP_HEADING(new_lvl)

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
    term = fake.word().capitalize()
    lines.append(term)
    has_inline_markup = LAMGEN_DECISION(50)
    definition = [f": {generate_sentence(state, has_inline_markup)}" for _ in LAM_RANDOM_RANGE(1,3)]
    lines.extend(definition)
    return SCAFFOLD_JOINLINES(lines)


def generate_footnote(state:State=None):
    """
    index: random number
    content: words, sentences, blocks
    """
    lines = []

    index = f"[^{state.footnote_index}]:"
    state.footnote_index+=1

    content = generate_sub_content(state, is_indented=True)

    lines.append(index)
    lines.append(content)

    return SCAFFOLD_JOINLINES(lines)


def generate_admonition(state:State=None):
    """
    type: choice
    title: words
    content: words, sentences, blocks
    """
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

def generate_heading(state:State=None, level:int=0):
    """
    level: integer
    content: words, inline markup
    """
    if not level:
        level = "#"*state.heading_level
        state.heading_level = adjust_heading_level(state.heading_level)
    else:
        level = "#"*level
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


def generate_markdown_post(state:State=None, num_blocks:int=0):
    generator_funcs = create_generators()
    blocks = []
    if not num_blocks:
        num_blocks = random.randint(3,20)
    
    blocks.append(generate_meta(state))
    blocks.append(generate_heading(state, 1))
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
    for i in range(5):
        print(f"##################################################")
        print(f"Post {i} ###########################################")
        print(f"##################################################")
        print(generate_markdown_post(current_state))
        print("\n")
        
def run_single_generator():
    current_state = State()
    for i in range(5):
        print(generate_olist(current_state))
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
#run_generator()
run_single_generator()
#run_get_sentences()
#run_generators()
#%%
