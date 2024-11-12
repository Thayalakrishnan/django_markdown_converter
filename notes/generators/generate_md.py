#%%
import random
from faker import Faker
from typing import Callable

from notes.generators.generate_base import block_generator

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

LAM_FUNC_NAMNE = lambda func: func.__name__.split("_")[1]

def construct_list(items:list=[]) -> str:
    #print("[construct_list]")
    lines = []
    for item in items:
        #print(item)
        ind, mark, content = item
        mark = f"{mark} " if mark == "-" else f"{mark}. "
        lines.append(f"{' '*ind}{mark}{content}")
    return SCAFFOLD_JOINLINES(lines)

def indent_content(content:str="") -> str:
    return "\n".join([INDENT + _ for _ in content.split("\n")])

def construct_sub_content(content, is_indented:bool=False) -> str:
    if isinstance(content, str):
        if is_indented:
            return indent_content(content)
        return content
    elif isinstance(content, list):
        #content = construct_markdown_blocks(num_blocks=num_blocks, is_nested=False, has_meta=False)
        content = "yeet"
    return content

def join_table_row(row):
    return f"| {' | '.join(row)} |"

def construct_table_row(size:int=0):
    row = [LAMGEN_FAKE_WORDS(1,3) for _ in range(size)]
    return join_table_row(row)

######################
"""
Generators
structure: 
name, content, attributes
"""
def construct_attributes(props:list=[]) -> str:
    #print("[construct_attributes] Start")
    attrs = [f"{k}=\"{v}\"" for k,v in props]
    joined = LAM_SPACED_JOIN(attrs)
    #print("[construct_attributes] End")
    return SCAFFOLD_ATTRS(joined)

def construct_meta(data:dict={}) -> str:
    """
    """
    pairs = data.get("pairs", [])
    attrs = [f"{k}: {v}" for k,v in pairs]
    return SCAFFOLD_META(attrs)

def construct_code(data:dict={}) -> str:
    """
    language: random
    content: lines of sentences
    """
    language = data.get("language", "")
    content = data.get("content", [])
    
    lines = []
    header = "```" if language else f"```{language}"
    lines.append(header)
    lines.extend(content)
    lines.append("```")
    return SCAFFOLD_JOINLINES(lines)


def construct_dlist(data:dict={}) -> str:
    """
    term: random word or words
    definition: words, sentences, blocks, inline markup
    """
    lines = []
    
    term = data.get("term", "")
    lines.append(term)
    
    definition = data.get("definition", [])
    definition = [f": {_}" for _ in definition]
    lines.extend(definition)
    return SCAFFOLD_JOINLINES(lines)


def construct_footnote(data:dict={}) -> str:
    """
    index: random number
    content: words, sentences, blocks
    """
    lines = []
    index = f"[^{data.get('index', 1)}]:"
    
    content = data.get("content", [])
    content = construct_sub_content(content, is_indented=True)

    lines.append(index)
    lines.append(content)
    return SCAFFOLD_JOINLINES(lines)


def construct_admonition(data:dict={}) -> str:
    """
    type: choice
    title: words
    content: words, sentences, blocks
    """
    lines = []
    header = ["!!!"]
    ad_type = data.get("type", "")
    ad_title = data.get("title", "")
    if ad_type:
        header.append(ad_type)
    if ad_title:
        header.append(f'\"{ad_title}\"')
    
    content = data.get("content", [])
    content = construct_sub_content(content, is_indented=True)
    
    lines.append(LAM_SPACED_JOIN(header))
    lines.append(content)
    return SCAFFOLD_JOINLINES(lines)


def construct_table(data:dict={}) -> str:
    """
    header: random number of columns
    body: random number of rows and use columns
    - cells: inline markup
    """
    lines = []

    header = data.get("header", [])
    header = join_table_row(header)
    lines.append(header)
    
    breaker = data.get("break", [])
    breaker = join_table_row(breaker)
    lines.append(breaker)
    
    body = data.get("body", [])
    for row in body:
        lines.append(join_table_row(row))
        
    return SCAFFOLD_JOINLINES(lines)

def construct_hr(data:dict={}) -> str:
    content = data.get("content", "***")
    return content

def construct_heading(data:dict={}) -> str:
    """
    level: integer
    content: words, inline markup
    """
    level = data.get("level", 2)
    content = data.get("content", "Heading Content")
    return f"{'#'*level} {content}"

def construct_image(data:dict={}) -> str:
    """
    alt: words
    title: words
    src: url
    """
    alt = data.get("alt", "")
    title = data.get("title", "")
    src = data.get("src", "")
    return f"![{alt}]({src} \"{title}\")"

def construct_svg(data:dict={}) -> str:
    """
    content: xml
    """
    content = data.get("content", "")
    return LAM_HTML_TAG("svg", content)

def construct_html(data:dict={}) -> str:
    """
    tag: word
    content: xml
    """
    tag = data.get("tag", "")
    content = data.get("content", "")
    return LAM_HTML_TAG(tag, content)

def construct_ulist(data:dict={}) -> str:
    """
    content: list item: words, sentences, blocks
    """
    items = data.get("items", [])
    return construct_list(items)

def construct_olist(data:dict={}) -> str:
    """
    content: list item: words, sentences, blocks
    """
    items = data.get("items", [])
    return construct_list(items)

def construct_blockquote(data:dict={}) -> str:
    """
    content: words, sentences, blocks
    """
    content = data.get("content", "")
    content = construct_sub_content(content, is_indented=False)
    lines = ["> " + line for line in content.split("\n")]
    return SCAFFOLD_JOINLINES(lines)

def construct_paragraph(data:dict={}) -> str:
    """
    content: sentences
    """
    content = data.get("content", "")
    return content

def construct_emptyline(data:dict={}) -> str:
    return "\n\n"

def construct_newline(data:dict={}) -> str:
    return "\n"

def construct_none(data:dict={}) -> str:
    return ""

##################################
"""
Generators
"""
def create_constructors() -> dict:
    generators = [
        construct_meta,
        construct_code,
        construct_dlist,
        construct_footnote,
        construct_admonition,
        construct_table,
        construct_hr,
        construct_heading,
        construct_image,
        construct_svg,
        construct_html,
        construct_ulist,
        construct_olist,
        construct_blockquote,
        construct_paragraph,
    ]
    ret = {}
    for func in generators:
        name = LAM_FUNC_NAMNE(func)
        ret.update({name: func})
    return ret


def construct_block(block:tuple=()) -> str:
    name, data, props = block
    #print(f"[construct_block] Start: {name}")
    constructor_funcs = create_constructors()
    func = constructor_funcs.get(name, lambda x: x)
    md = func(dict(data))
    if props:
        attrs = construct_attributes(props)
        #print(f"[construct_block] End: {name}")
        return md + "\n" + attrs
    #print(f"[construct_block] End: {name}")
    return md


def construct_markdown():
    constructor_funcs = create_constructors()
    blocks = block_generator()
    
    doco = []
    for block in blocks:
        #print(block)
        md_block = construct_block(block)
        #print(md_block)
        doco.append(md_block)
    
    print("\n\n".join(doco))
    return doco

construct_markdown()
