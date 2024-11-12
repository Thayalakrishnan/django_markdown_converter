#%%
import random
from faker import Faker
from collections import OrderedDict
from typing import Union

fake = Faker()

LAM_JOIN = lambda sep="", x=[]: sep.join(x)
LAM_SPACED_JOIN = lambda x=[]: LAM_JOIN(" ", x)
LAM_RANDOM_INT = lambda l,u: random.randint(l,u)
LAM_RANDOM_RANGE = lambda l,u: range(LAM_RANDOM_INT(l,u))
LAMGEN_DECISION = lambda w=50: random.randint(1,100) < w

class State:
    INLINE_MARKUP_LIST = [
        ("code" ,("`", "`",)),
        ("samp" ,("``", "``",)),
        ("bold" ,("**", "**",)),
        ("em" ,("_", "_",)),
        ("emoji" ,(":", ":",)),
        ("sup" ,("^", "^",)),
        ("sub" ,("~", "~",)),
        ("math" ,("$", "$",)),
        ("del" ,("--", "--",)),
        ("mark" ,("==", "==",)),
        #("link" , ("<", ">",)),
    ]
    SENTENCE_ENDINGS = ["."]*10 + ["!"]*3 + ["?"]*2 + [";"]*1

    def __init__(self):
        self.heading_level = 2
        self.footnote_index = 1
        self.footnote_count = 0
        self.inline_markup_count = 0
        self.current_depth = 0
        self.inline_markup_list = [_[1] for _ in self.INLINE_MARKUP_LIST]

"""
## not
"footnote": lambda x: f"[^{x}]",
"link": lambda x: f"{x.get('title', '')}]({x.get('to', '')}",
"""
def markup_positions(minimum:int=0, maximum:int=25, pairs:int=0) -> list:
    spots = random.sample(range(minimum, maximum),k=pairs*2)
    spots.sort()
    positions = [(spots[i], spots[i+1]) for i in range(0,len(spots)-1, 2)]
    return positions

def nested_markup_position(minimum:int=0, maximum:int=25) -> list:
    if maximum - minimum > 1:
        return markup_positions(minimum, maximum, 1)[0]
    return (minimum, maximum)

def remainder_choices(choices:list=[], num_choices:int=0) -> tuple:
    all_choices = random.sample(choices, k=num_choices)
    remainder_choices = list(filter(lambda x: x not in all_choices, choices))
    return all_choices, remainder_choices


def markup_choices(choices:list=[], num_words:int=0) -> tuple:
    upper_range = num_words//7

    num_straight_choices = random.randint(0, upper_range)
    num_nested_choices = num_straight_choices//2

    straight_choices, leftover_choices = remainder_choices(choices, num_straight_choices)
    nested_choices = random.sample(leftover_choices, k=num_nested_choices)
    return straight_choices, nested_choices

def combine_choices(positions:list=[], straight_choices:list=[], nested_choices:list=[]) -> list:
    """(position, format)"""
    combined_choices = []
    for current_pos, current_straight in zip(positions, straight_choices):
        if len(nested_choices):
            nested_pos = nested_markup_position(current_pos[0], current_pos[1])
            combined_choices.append((nested_pos, nested_choices.pop()))
        combined_choices.append((current_pos, current_straight))
    return combined_choices


def generate_markedup_words(state:State=None, num_words:int=0):
    words = fake.words(nb=num_words)

    # markup choices
    straight_choices, nested_choices = markup_choices(state.inline_markup_list, num_words)

    # positions for straight choices
    positions = markup_positions(0, num_words, len(straight_choices))

    # combinding the straight and the nested chioces and positions
    combined = combine_choices(positions, straight_choices, nested_choices)

    # loop over the words and add in the formatting
    for pos, markup in combined:
        words[pos[0]] = markup[0] + words[pos[0]]
        words[pos[1]] =  words[pos[1]] + markup[1]
    return words


def generate_words(state:State=None, has_markup:bool=True, as_list:bool=False) -> Union[list, str]:
    num_words = random.randint(9, 25)
    words = generate_markedup_words(state, num_words) if has_markup else fake.words(nb=num_words)
    if as_list:
        return words
    return " ".join(words)

def generate_sentence(state:State=None, has_markup:bool=True, as_list:bool=False) -> Union[list, str]:
    words = generate_words(state, has_markup, as_list=True)
    # sentence endings
    ending = random.choice(state.SENTENCE_ENDINGS)
    #words.append(ending)
    words[0] = words[0].capitalize()
    words[-1] = words[-1] + ending
    if as_list:
        return words
    return " ".join(words)

def generate_sentences(state:State=None, has_markup:bool=True, as_list:bool=False) -> Union[list, str]:
    sentences = [generate_sentence(state, has_markup, as_list=False) for _ in LAM_RANDOM_RANGE(2,6)]
    if as_list:
        return sentences
    return LAM_SPACED_JOIN(sentences)

def generate_text(state:State=None, form:str="words", has_markup:bool=True):
    """
    text_type: words, sentence, sentences,
    has_markup: bool
    """
    if form == "sentence":
        return generate_sentence(state, has_markup)
    elif form == "sentences":
        return generate_sentences(state, has_markup)
    return generate_words(state, has_markup)


def run_single_generator():
    current_state = State()
    for i in range(1):
        print(generate_text(current_state, form="sentences", has_markup=True))

run_single_generator()
#%%
