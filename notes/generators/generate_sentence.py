#%%
import random
from faker import Faker
from collections import OrderedDict


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
def generate_plain_sentence(state:State=None, sentence_length:int=1):
    return [fake.word() for w in range(sentence_length)]

def generate_markedup_sentence(state:State=None, sentence_length:int=1):
    stack = OrderedDict()
    words = []
    inline_markup_dict = dict(state.INLINE_MARKUP_LIST)

    for w in range(sentence_length):
        words.append(" ")

        # open inline formatting
        if (LAMGEN_DECISION(10)) or (len(stack) and LAMGEN_DECISION(50)):
            key = random.choice(list(inline_markup_dict.keys()))
            value = inline_markup_dict.pop(key)
            stack.update({key: value})
            words.append(value[0])

        word = fake.word()
        words.append(word)

        # close inline formatting
        if len(stack) and LAMGEN_DECISION(90):
            key, value = stack.popitem(last=False)
            words.append(value[1])
            inline_markup_dict.update({key: value})

    while len(stack):
        key, value = stack.popitem(last=False)
        words.append(value[1])
    return words


def generate_markedup_sentence_optimized(state:State=None, sentence_length:int=1):
    stack = OrderedDict()
    stack = []
    words = []

    num_inline_markup = random.randint(1,5)
    markup_choices = random.sample(state.INLINE_MARKUP_LIST, k=num_inline_markup)

    while len(markup_choices) or len(stack):
        """
        each loop we add a word
        we also have the change to add some inline formatting
        """

        words.append(" ")

        # open inline formatting
        if len(markup_choices) and ((LAMGEN_DECISION(10)) or (len(stack) and LAMGEN_DECISION(50))):
            markup = markup_choices.pop()
            key, value = markup
            stack.append(value[1])
            words.append(value[0])

        word = fake.word()
        words.append(word)

        # close inline formatting
        if len(stack) and LAMGEN_DECISION(90):
            value = stack.pop()
            words.append(value)

    return "".join(words)


def sentence_positions(minimum:int=0, maximum:int=25, pairs:int=0) -> list:
    spots = random.sample(range(minimum, maximum),k=pairs*2)
    spots.sort()
    positions = [(spots[i], spots[i+1]) for i in range(0,len(spots)-1, 2)]
    return positions

def nested_position(minimum:int=0, maximum:int=25) -> list:
    return sentence_positions(minimum, maximum, 1)[0]

def is_nested(maximum:int=25, pairs:int=0) -> list:
    spots = random.sample(range(0,maximum),k=pairs*2)
    spots.sort()
    positions = [(spots[i], spots[i+1]) for i in range(0,len(spots)-1, 2)]
    return positions

def generate_markedup_sentence_moreoptimized(state:State=None):
    sentence_min = 9
    sentence_max = 25
    sentence_length = random.randint(sentence_min, sentence_max)
    words = fake.words(nb=sentence_length)

    upper_range = sentence_length//7
    num_inline_s_mu = random.randint(0, upper_range)
    num_inline_nested_mu = num_inline_s_mu//2

    mu_choices = random.sample(state.inline_markup_list, k=num_inline_s_mu)
    if num_inline_nested_mu:
        nested_choices = random.sample(mu_choices, k=num_inline_nested_mu)
    else:
        nested_choices = []

    straight_choices = list(filter(lambda x: x not in nested_choices, mu_choices))
    positions = sentence_positions(0, sentence_length, len(straight_choices))

    #print(f"straight_choices {type(straight_choices)}")
    #print(straight_choices)
    #print(f"nested_choices {type(nested_choices)}")
    #print(nested_choices)
    #print(f"positions {type(positions)}")
    #print(positions)

    for current_pos, current_straight in zip(positions, straight_choices):
        #key, value = current_straight
        if len(nested_choices):
            current_nested = nested_choices.pop()
            #nested_key, nested_value = current_nested
            nested_start, nested_stop = current_nested
            nested_pos = nested_position(current_pos[0], current_pos[1])
            words[nested_pos[0]] = nested_start + words[nested_pos[0]]
            words[nested_pos[1]] =  words[nested_pos[1]] + nested_stop
        
        start, stop = current_straight
        words[current_pos[0]] = start + words[current_pos[0]]
        words[current_pos[1]] =  words[current_pos[1]] + stop
        

    return " ".join(words)


def generate_sentence(state:State=None, has_inline_markup:bool=True):
    words = generate_markedup_sentence(state) if has_inline_markup else generate_markedup_sentence(state)
    ending = random.choice(state.SENTENCE_ENDINGS)
    words.append(ending)
    return "".join(words)

def generate_sentences(state:State=None, has_inline_markup:bool=True):
    sentences = [generate_sentence(state, has_inline_markup) for _ in LAM_RANDOM_RANGE(1,6)]
    return LAM_SPACED_JOIN(sentences)

def run_single_generator():
    current_state = State()
    for i in range(1):
        print(generate_markedup_sentence_moreoptimized(current_state))

run_single_generator()
#%%
