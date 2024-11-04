#%%
import random
from faker import Faker

fake = Faker()

INDENT = "    "
WEIGHTED_CHOICE = [1]*10 + [2]*8 + [3]*4 + [4]*2

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)

SCAFFOLD_JOINLINES = lambda x=[]: "\n".join(x)
SCAFFOLD_FENCED = lambda o="", x=[],c="": "\n".join([o, *x, c, ""])
SCAFFOLD_META = lambda x=[]: SCAFFOLD_FENCED("---", x,"---")
#SCAFFOLD_FOOTNOTE = lambda index=0, x=[]: SCAFFOLD_FENCED(f"[^{index}]:", x,"")
#SCAFFOLD_ADMONITION = lambda ty="", ti="", x=[]: SCAFFOLD_FENCED(f"!!! {ty} {ti}", x,"")

LAM_HTML_TAG = lambda x,b: f"<{x}>{b}</{x}>"
LAM_RANDOM_RANGE = lambda l,u: range(random.randint(l,u))

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


def random_decision(weight:int=50):
    """the higher the number, the more likely it is to be yes"""
    return random.randint(1,100) < weight

def generate_list_item(listtype:str="ulist", level:int=0, counter:int=1, content:str=""):
    indent = level*' '*4
    delimter = "- " if listtype == "ulist" else f"{counter}. "
    if not content:
        content = random_words(1,6).capitalize()
    
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
        
        if random_decision():
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
    if random_decision():
        while len(stack):
            indent_counter-=1
            current_counter = stack.pop()
            items.append(generate_list_item(listtype, indent_counter, current_counter))
    return SCAFFOLD_JOINLINES(items)

def generate_fake_sentences():
    return " ".join(fake.sentences(nb=random.randint(1,3)))

def generate_indented_content():
    content = []
    for i in range(random.choice(WEIGHTED_CHOICE)):
        content.append(INDENT + generate_fake_sentences())
        content.append(INDENT + "")
    content.pop()
    return content


def random_words(lower:int=1, upper:int=2):
    return LAM_SPACED_JOIN(fake.words(nb=random.randint(lower,upper)))

def join_table_row(row):
    return f"| {' | '.join(row)} |"

def generate_table_row(size:int=0):
    row = [random_words(1,3) for _ in range(size)]
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
def insert_inline_markup() -> bool:
    return random_decision() and random_decision() and random_decision()

def close_inline_markup(stack:list=[]) -> bool:
    return len(stack) and (random_decision() or random_decision() or random_decision())

def generate_sentence(state:State=None):
    sentence_length = random.randint(5,20)
    stack = []
    words = []
    inline_markup = state.INLINE_MARKUP_LIST
    
    for w in range(sentence_length):
        word = fake.word()
        
        if insert_inline_markup():
            imarkup = random.choice(inline_markup)
            if imarkup not in stack:
                stack.append(imarkup)
                word = imarkup[0] + word
                
        if close_inline_markup(stack):
            imarkup = stack.pop()
            word = word + imarkup[1]
        words.append(word)
        
    while len(stack):
        imarkup = stack.pop()
        words[-1]+=imarkup[1]
        
    ending = random.choice(state.SENTENCE_ENDINGS)
    words[-1]+=ending
    return " ".join(words)

######################

def generate_meta(state:State=None):
    """
    generate the key value pairs
    - generate random number of lines
    - might have types later, but for now just single word paired
    with some ofther words
    """
    pairs = [f"{fake.word()}: {' '.join(fake.words())}" for _ in range(random.randint(1,5))]
    return SCAFFOLD_META(pairs)

def generate_code(state:State=None):
    """
    language: random
    content: random
    """
    lines = []
    header = ["```"]
    if random_decision(80):
        language = random.choice(["python", "javascript", "c", "cpp", "assembly", "css", "html"])
        header.append(language)
        
    lines.append(LAM_JOIN("", header))
    
    max_lines = random.randint(1,20)
    for i in range(max_lines):
        lower = random.randint(2,5)
        upper = lower + random.randint(1,5)
        lines.append(random_words(lower, upper))
        extra_line_break = random_decision() and random_decision() and random_decision()
        if extra_line_break:
            lines.append("\n")
    lines.append("```")
    return SCAFFOLD_JOINLINES(lines)

def generate_dlist(state:State=None):
    """
    term: random word
    definition:
    - random number of sentences
    - random sentences
    """
    term = [fake.word().capitalize()]
    definition = [f": {fake.sentence(nb_words=10)}" for _ in range(random.randint(1,3))]
    term.extend(definition)
    return SCAFFOLD_JOINLINES(term)

def generate_footnote(state:State=None):
    """
    index: random number
    content:
    - random number of paragraphs
    - random number of sentences per paragraph
    - possible random other blocks of content
    """
    lines = []

    index = f"[^{state.footnote_index}]:"
    state.footnote_index+=1

    content = generate_indented_content()

    lines.append(index)
    lines.extend(content)
    return SCAFFOLD_JOINLINES(lines)


def generate_admonition(state:State=None):
    """
    type: random type from list
    title: random words
    content:
    - random number of paragraphs
    - random number of sentences per paragraph
    - possible random other blocks of content
    """
    lines = []
    header = ["!!!"]
    if random_decision(80):
        ad_type = random.choice(["note", "info", "warning", "tip", "danger", "example"])
        header.append(ad_type)
    if random_decision(80):
        header.append(f'\"{random_words(1,3)}\"')

    lines.append(LAM_SPACED_JOIN(header))
    content = generate_indented_content()
    lines.extend(content)
    return SCAFFOLD_JOINLINES(lines)


def generate_table(state:State=None):
    """
    header: random number of columns
    body: random number of rows and use columns
    """
    lines = []
    cols = random.randint(1,10)
    rows = random.randint(1,10)

    header = generate_table_row(cols)
    lines.append(header)

    breaker = join_table_row(["---"]*cols)
    lines.append(breaker)

    for i in range(rows):
        lines.append(generate_table_row(cols))
    return SCAFFOLD_JOINLINES(lines)


def generate_hr(state:State=None):
    if random_decision(80):
        return "***"
    return "---"

def generate_heading(state:State=None):
    """
    level: random level from range
    content: random words | possible inline markup
    """
    level = "#"*state.heading_level
    state.heading_level = adjust_heading_level(state.heading_level)
    content = random_words(1,6).capitalize()
    return f"{level} {content}"

def generate_image(state:State=None):
    alt = fake.sentence(nb_words=10)
    title = fake.sentence(nb_words=10)
    src = fake.image_url()
    return f"![{alt}]({src} \"{title}\")"

def generate_svg(state:State=None):
    """
    content
    """
    content = random_words(5,10)
    return LAM_HTML_TAG("svg", content)

def generate_html(state:State=None):
    """
    tag: random word
    content: just random html
    """
    tag = fake.word()
    content = random_words(5,10)
    return LAM_HTML_TAG(tag, content)

def generate_ulist(state:State=None):
    """
    """
    return generate_list(state, "ulist")

def generate_olist(state:State=None):
    """
    """
    return generate_list(state, "olist")

def generate_blockquote(state:State=None):
    """
    content:
    - random number of lines
    - determine if nested
    - max depth 2 i reckon
    """
    lines = ["> " + random_words(5,10) for _ in LAM_RANDOM_RANGE(1,5)]
    return SCAFFOLD_JOINLINES(lines)

def generate_emptyline(state:State=None):
    return "\n\n"

def generate_newline(state:State=None):
    return "\n"

def generate_none(state:State=None):
    return ""

def generate_paragraph(state:State=None):
    """
    content
    """
    num_sentences = random.randint(1,6)
    lines = []
    for _ in range(num_sentences):
        lines.append(generate_sentence(state))
    return LAM_SPACED_JOIN(lines)


GENERATORS = [
    #generate_meta,
    generate_code,
    generate_dlist,
    generate_footnote,
    generate_admonition,
    generate_table,
    generate_hr,
    #generate_heading,
    generate_image,
    generate_svg,
    generate_html,
    generate_ulist,
    generate_olist,
    generate_blockquote,
    #generate_emptyline,
    #generate_newline,
    #generate_none,
    generate_paragraph,
]

NESTED_GENERATORS = [
    generate_code,
    generate_dlist,
    generate_admonition,
    generate_table,
    generate_hr,
    generate_image,
    generate_svg,
    generate_html,
    generate_ulist,
    generate_olist,
    generate_blockquote,
    generate_paragraph,
]

def run_generators():
    current_state = State()
    for _ in GENERATORS:
        name = _.__name__.split("_")[1]
        print(f"## {name}\n")
        print(_(current_state))
        print("\n")


def run_generator():
    current_state = State()
    for i in range(20):
        #print(repr(generate_code(current_state)))
        #print(f"loop {i} #########################")
        print(generate_olist(current_state))
        #generate_code(current_state)
        print("\n")


def run_get_sentences():
    current_state = State()
    for i in range(5):
        print(generate_sentence(current_state))


def make_markdown_block():
    current_state = State()
    blocks = []
    num_blocks = random.randint(3,20)
    blocks.append(generate_heading(current_state))
    # has meta
    has_meta = random_decision()
    if has_meta:
        blocks.append(generate_meta(current_state))
    
    for i in range(num_blocks):
        
        has_heading = random_decision()
        
        if has_heading:
            blocks.append(generate_heading(current_state))
            
        generator = random.choice(GENERATORS)
        blocks.append(generator(current_state))
    
    return "\n\n".join(blocks)

print(make_markdown_block())
#run_generator()
#run_get_sentences()
#run_generators()

# %%
