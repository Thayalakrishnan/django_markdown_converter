#%%
import random
from faker import Faker

fake = Faker()

SMALL = "s"
MEDIUM = "m"
LARGE = "l"


INDENT = "    "
WEIGHTED_CHOICE = [1]*10 + [2]*8 + [3]*4 + [4]*2


LAM_JOIN = lambda x=[]: " ".join(x)

SCAFFOLD_JOINLINES = lambda x=[]: "\n".join(x)

SCAFFOLD_FENCED = lambda o="", x=[],c="": "\n".join([o, *x, c, ""])

SCAFFOLD_META = lambda x=[]: SCAFFOLD_FENCED("---", x,"---")
SCAFFOLD_FOOTNOTE = lambda index=0, x=[]: SCAFFOLD_FENCED(f"[^{index}]:", x,"")
SCAFFOLD_ADMONITION = lambda ty="", ti="", x=[]: SCAFFOLD_FENCED(f"!!! {ty} {ti}", x,"")

CURRENT_HEADING_LEVEL = 2

LAM_HTML_TAG = lambda x,b: f"<{x}>{b}</{x}>"
LAM_RANDOM_RANGE = lambda l,u: range(random.randint(l,u))

class State:
    def __init__(self):
        self.heading_level = 2
        self.footnote_index = 1


def random_boolean():
    return random.randint(1,100) < 80

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
    language
    lines.append("```")
    return ""

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

def generate_fake_sentences():
    return " ".join(fake.sentences(nb=random.randint(1,3)))

def generate_indented_content():
    content = []
    for i in range(random.choice(WEIGHTED_CHOICE)):
        content.append(INDENT + generate_fake_sentences())
        content.append(INDENT + "")
    content.pop()
    return content

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

def random_words(lower:int=1, upper:int=2):
    return LAM_JOIN(fake.words(nb=random.randint(lower,upper)))

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
    if random_boolean():
        header.append(fake.word())
    if random_boolean():
        header.append(f'\"{random_words(1,3)}\"')

    lines.append(LAM_JOIN(header))
    content = generate_indented_content()
    lines.extend(content)
    return SCAFFOLD_JOINLINES(lines)

def join_table_row(row):
    return f"| {' | '.join(row)} |"

def generate_table_row(size:int=0):
    row = [random_words(1,3) for _ in range(size)]
    return join_table_row(row)


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
    print(lines)
    return SCAFFOLD_JOINLINES(lines)


def generate_hr(state:State=None):
    if random_boolean():
        return "***"
    return "---"


def adjust_heading_level(lvl:int=2) -> int:
    new_lvl = lvl + random.choice([-1, 0, 0, 1, 1])
    #print(new_lvl)
    if new_lvl < 2:
        return 2
    if new_lvl > 6:
        return 6
    return new_lvl


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
    content:
    - random number of items
    - for each item determine if has nested
    - if nested determine how many items, maybe minimum 3
    - maximum depth of maybe 3
    """
    return ""

def generate_olist(state:State=None):
    """
    content:
    - random number of items
    - for each item determine if has nested
    - if nested determine how many items, maybe minimum 3
    - maximum depth of maybe 3
    """
    return ""

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

def generate_paragraph(state:State=None, size:str="m"):
    """
    content
    """
    if size == SMALL:
        return fake.paragraph(nb_sentences=2, variable_nb_sentences=False)
    if size == MEDIUM:
        return fake.paragraph(nb_sentences=3, variable_nb_sentences=False)
    if size == LARGE:
        return fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
    return fake.paragraph(nb_sentences=3, variable_nb_sentences=False)


GENERATORS = [
    generate_meta,
    generate_code,
    generate_dlist,
    generate_footnote,
    generate_admonition,
    generate_table,
    generate_hr,
    generate_heading,
    generate_image,
    generate_svg,
    generate_html,
    generate_ulist,
    generate_olist,
    generate_blockquote,
    generate_emptyline,
    generate_newline,
    generate_none,
    generate_paragraph,
]

def run_generators():
    current_state = State()
    for _ in GENERATORS:
        name = _.__name__.split("_")[1]
        print(f"{name}--------------------------")
        #print(repr(_(current_state)))
        print(_(current_state))


def run_generator():
    current_state = State()
    for i in range(10):
        print(repr(generate_blockquote(current_state)))
        print("\n")



run_generators()

# %%
