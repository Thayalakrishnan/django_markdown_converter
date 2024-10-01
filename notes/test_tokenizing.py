#%%
import re

CASES = [
    ["code",      [("`", "`")]], # can nest
    ["strong",    [("**", "**"), ("__", "__")]], # can nest
    ["em",        [("*", "*"), ("_", "_")]], # can nest
    ["del",       [("~~", "~~"), ("--", "--")]], # can nest
    ["mark",      [("==", "==")]], # can nest
    ["samp",      [("``", "``")]], # can nest
    ["sup",       [("^", "^")]], # can nest
    ["sub",       [("~", "~")]], # can nest
    ["navlink",   [("<navlink ", "</navlink>")]], # can nest

    ["text",      [("", "")]], # can nest

    ["emoji",     [(":", ":")]], # cannot nest
    ["math",      [("$", "$")]], # cannot nest
    ["rawlink",   [("<", ">")]], # cannot nest
    ["footnote",  [("[^", "]")]], # cannot nest
    ["link",      [("[", ")")]], # cannot nest
]

TOKENS = [
    ("code", "`", "`"),
    ("em", "*", "*"),
    ("strong", "**", "**"),
    ("em", "_", "_"),
    ("strong", "__", "__"),
    ("del", "~~", "~~"),
    ("del", "--", "--"),
    ("mark", "==", "=="),
    ("samp", "``", "``"),
    ("emoji", ":", ":"),
    ("sup", "^", "^"),
    ("sub", "~", "~"),
    ("math", "$", "$"),
    ("link", "<", ">"),
    ("footnote", "[^", "]"),
    ("link", "[", ")")
]



lambda_extractor = lambda pat: lambda x: x[len(pat[0]):len(pat[1])*(-1)]
lambda_formatter = lambda pat: lambda x: f"{pat[0]}{x}{pat[1]}"

# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})"
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>

# processing content
get_text_captured = lambda cur, content: content[cur[0]:cur[1]]
get_text_between = lambda pre, cur, content: content[pre[1]:cur[0]]
get_text_after = lambda cur, content: content[cur[1]::]
create_text_object = lambda content: {"type": "text", "data": content}
create_markup_object = lambda name, content, lookup: {"type": name, "data": lookup[name](content)}



TOKEN_LIST = [
    "`{1,2}",
    "*{1,3}",
    "_{1,3}",
    "~{1,2}",
    "-{1,2}",
    "={1,2}",
    ":{1}",
    "^{1}",
    "${1}",
    "<{1}",
]
"""
(?P<tick>`{1,2})|
(?P<asterisk>*{1,3})|
(?P<underscore>_{1,3})|
(?P<tilde>~{1,2})|
(?P<dash>-{1,2})|
(?P<assign>={1,2})|
(?P<colon>:{1})|
(?P<caret>^{1})|
(?P<dollar>${1})|
(?P<less><{1})|

(?P<tick>`{1,2})|(?P<asterisk>*{1,3})|(?P<underscore>_{1,3})|(?P<tilde>~{1,2})|(?P<dash>-{1,2})|(?P<assign>={1,2})|(?P<colon>:{1})|(?P<caret>^{1})|(?P<dollar>${1})|(?P<less><{1})
"""


#%%
TOKENIZER_LIST = "(?P<tick>`{1,2})|(?P<asterisk>\*{1,2})|(?P<underscore>_{1,3})|(?P<tilde>~{1,2})|(?P<dash>-{1,2})|(?P<assign>={1,2})|(?P<colon>:{1})|(?P<caret>\^{1})|(?P<dollar>\${1})|(?P<less><{1})|(?P<text>\w+)"
TOKENIZER = re.compile(TOKENIZER_LIST)

MD = [
    """**Markdown Example** with _**Inline Markup**_.""",
    """This is a **bold** statement, and this is an _italicized_ one.""",
    """You can even combine them to make text _**both italic and bold**_.""",
    """If you need to reference a link, here's a [link to Markdown documentation](https://www.markdownguide.org).""",
    """This item has some inline markup like _italics_ and **bold** text.""",
    """Nested list item with a [link to a website](https://example.com) and some `inline code`.""",
    """Even deeper nesting: _Italicized_ **bold** list item with `code` inline.""",
    """Another item with **nested** inline **markup**.""",
    """This list item uses some `inline code` and ends with _**italicized and bold**_ text.""",
    """To write code, you can use backticks for `inline code`, like this.""",
]

def create_tokenizer(tokens):
    TOKEN_LIST
    pass


MD = " ".join(MD)
MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "
SOLUTION = [
    "*",
    "**",
    "Markdown Example",
    "**",
    "with",
    "*",
    "but we could keep going and going ",
    "*",
    "till there is another one",
    "*",
    " italizczed. ",
]


matches = TOKENIZER.finditer(MD)

PATTERN_DICT = {}

text_groups = []
current_text_group = []

for match in matches:
    group = match.lastgroup
    content = match.group(group)
    
    if group == "text":
        current_text_group.append(content)
    else:
        if len(current_text_group):
            text_groups.extend([" ".join(current_text_group), content])
            
        else:
            text_groups.extend([content])
        current_text_group = []
print(text_groups)
print("done")

#%%



TOKENIZER_LIST = "(?P<asterisk2>\*{2})|(?P<asterisk1>\*{1})|(?P<text>\w+)"
TOKENIZER_LIST = "(?P<asterisk2>\*{2}(?=.+?\*{2}))|(?P<asterisk1>\*{1})|(?P<text>\w+)"
TOKENIZER = re.compile(TOKENIZER_LIST)

MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "
matches = TOKENIZER.finditer(MD)

PATTERN_DICT = {
    "tick": 0,
    "asterisk": 0,
    "underscore": 0,
    "tilde": 0,
    "dash": 0,
    "assign": 0,
    "colon": 0,
    "caret": 0,
    "dollar": 0,
    "less": 0,
}

text_root = {"type": "root", "data": []}
current_text_group = text_root
current_text_group_ptr = text_root["data"]


for match in matches:
    group = match.lastgroup
    content = match.group(group)
    
    if group == "text":
        current_text_group_ptr.append(content)
    else:
        #size = len(match.group(group))
        # if the counter is > 0 we might have a match
        if PATTERN_DICT[group]:
            size = len(match.group(group))
            # if the size is less, we can close a group
            if size < PATTERN_DICT[group]:
                pass
            else:
                # if the size is more, we add to the group
                PATTERN_DICT[group] = PATTERN_DICT[group] + size
        
        if len(current_text_group):
            text_groups.extend([" ".join(current_text_group), content])
        else:
            text_groups.extend([content])
        current_text_group = []
        
    #print(f"{match.lastgroup} | {size}")
print(text_groups)
print("done")

# %%
import re

def md_string_tokenizer(pattern, source):
    matches = pattern.finditer(source)
    current_text_group = []

    for match in matches:
        token = match.lastgroup
        content = match.group(token)
        #print(match.groupdict())
        if token == "text":
            current_text_group.append(content)
        else:
            if len(current_text_group):
                yield ("text", " ".join(current_text_group))
                current_text_group = []
            yield (token, content)
    

TOKENIZER_LIST = "(?P<asterisk2>\*{2})|(?P<asterisk1>\*{1})|(?P<text>\w+)"
TOKENIZER = re.compile(TOKENIZER_LIST)
MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "
mdtokens = md_string_tokenizer(TOKENIZER, MD)




        
    
    #pass
# %%

BTRACKER = {
    "asterisk2": False,
    "asterisk1": False,
    #"text": False,
}

BTEXT = {
    "asterisk2": "",
    "asterisk1": "",
}


vals = [('asterisk2', '**'), ('asterisk1', '*'), ('text', 'Markdown Example'), ('asterisk2', '**'), ('text', 'with'), ('asterisk1', '*'), ('text', 'but we could keep going and going'), ('asterisk1', '*'), ('text', 'till there is another one'), ('asterisk1', '*')]
text_stack = []
nesting_stack = []
depth = 0
for token, value in vals:
    
    if token != "text":
        BTRACKER[token] = not BTRACKER[token]
        
        if BTRACKER[token]:
            depth+=1
            print(f"token {token} open | depth {depth}")
        else:
            depth-=1
            """
            when we close group , we need to gather all the objects in the 
            stack and nest them within the new object
            """
            print(f"token {token} closed | depth {depth}")
            if depth:
                pass
            else:
                nesting_stack.append({"type": token, "data": text_stack.pop()})
            
    else:
        text_stack.append(value)
        #print(value)
# %%
