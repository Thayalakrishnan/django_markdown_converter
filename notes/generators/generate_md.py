#%%
from faker import Faker

fake = Faker()

SMALL = "s"
MEDIUM = "m"
LARGE = "l"


scaffold_meta = lambda x=[]: "\n".join(["---", *x, "---", ""])


"""
"""


def generate_meta(size:str="m"):
    
    return ""

def generate_code(size:str="m"):
    return ""

def generate_dlist(size:str="m"):
    return ""

def generate_footnote(size:str="m"):
    return ""

def generate_admonition(size:str="m"):
    return ""

def generate_table(size:str="m"):
    return ""

def generate_hr(size:str="m"):
    return ""

def generate_heading(size:str="m"):
    return ""


def generate_image(size:str="m"):
    alt = fake.sentence(nb_words=10)
    title = fake.sentence(nb_words=10)
    src = fake.image_url()
    return f"![{alt}]({src} \"{title}\")"


def generate_svg(size:str="m"):
    return ""

def generate_html(size:str="m"):
    return ""

def generate_ulist(size:str="m"):
    return ""

def generate_olist(size:str="m"):
    return ""

def generate_blockquote(size:str="m"):
    return ""

def generate_emptyline(size:str="m"):
    return "\n\n"

def generate_newline(size:str="m"):
    return "\n"

def generate_none(size:str="m"):
    return ""


def generate_paragraph(size:str="m"):
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


for _ in GENERATORS:
    name = _.__name__.split("_")[1]
    print(f"{name}--------------------------")
    print(repr(_()))

# %%
scaffold_meta = lambda x=[]: "\n".join(["---", *x, "---", ""])

keyvaluepairs = ["name: lawen", "height: 186cm"]

print(scaffold_meta(keyvaluepairs))
# %%
