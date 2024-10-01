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

TOKENS = [
    ("samp", "``"),
    ("code", "`"),
    ("strong", "**", "__"),
    ("em", "*", "_"),
    ("del", "~~", "--"),
    ("mark", "=="),
    ("emoji", ":"),
    ("sup", "^"),
    ("sub", "~"),
    ("math", "$"),
    ("link", "<", ">"),
    ("footnote", "[^", "]"),
    ("link", "[", ")")
]

"""
(?P<samp>``)|
(?P<strong>(?:\*\*)|(?:__))|
(?P<del>(?:~~)|(?:--))|
(?P<mark>==)|
(?P<em>(?:\*)|(?:_))|
(?P<code>`)|
(?P<sup>\^)|
(?P<sub>~)|
(?P<math>\$)|
(?P<emoji>\:)|

(?P<link>(?:\<)|(?:\>))|
(?P<footnote>(?:\[\^)|(?:\]))|
(?P<link2>(?:\[)|(?:\)))|

(?P<tick>`{1,2})|(?P<asterisk>*{1,3})|(?P<underscore>_{1,3})|(?P<tilde>~{1,2})|(?P<dash>-{1,2})|(?P<assign>={1,2})|(?P<colon>:{1})|(?P<caret>^{1})|(?P<dollar>${1})|(?P<less><{1})


(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)|
(?P<footnote>(?:\[\^)|(?:\]))|(?P<link2>(?:\[)|(?:\)))|(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)|(?P<link>(?:\<)|(?:\>))
"""


#%%
import re


def md_string_tokenizer(pattern, source):
    matches = pattern.finditer(source)
    current_text_group = []

    for match in matches:
        token = match.lastgroup
        content = match.group(token)
        if token == "text":
            current_text_group.append(content)
        else:
            if len(current_text_group):
                yield ("text", "".join(current_text_group))
                current_text_group = []
            yield (token, content)
    
    yield ("text", "".join(current_text_group))
    

def create_tracker_from_tokenizer(tokenizer):
    ret = {}
    token_dict = tokenizer.groupindex.keys()
    for _ in token_dict:
        ret[_] = False
    return ret


def parse_inline_tokens(tokens, tracker):
    depth = 0
    object_stack = []
    root = {"type": "root", "data": []}
    current_object = root

    for token, value in tokens:
        
        if token != "text":
            # flip the switch
            tracker[token] = not tracker[token]
            
            # if the token is open
            if tracker[token]:
                # new open token, increase the depth
                depth+=1
                # create a new object
                new_object = {"type": "", "token": token, "data": []}
                # add the new object as a child to the current object
                current_object["data"].append(new_object)
                # add the current object to the stack
                object_stack.append(current_object)
                # assign the new object as the current object
                current_object = new_object
            else:
                # if the token is closed
                if depth:
                    if len(object_stack):
                        current_object["type"] = token
                        current_object["token"] = token
                        # if there is only one child element, just make that one child
                        # equal to it
                        if len(current_object["data"]) == 1:
                            current_object["data"] = current_object["data"].pop()
                        current_object = object_stack.pop()
                depth-=1
                
        else:
            current_object["data"].append({"depth": depth, "type": token, "data": value})
    return root["data"]

# %%
import re
import json


MD = """**Markdown Example** with _**Inline Markup**_.
This is a **bold** statement, and this is an _italicized_ one.
You can even combine them to make text _**both italic and bold**_.
If you need to reference a link, here's a [link to Markdown documentation](https://www.markdownguide.org).
This item has some inline markup like _italics_ and **bold** text.
Nested list item with a [link to a website](https://example.com) and some `inline code`.
Even deeper nesting: _Italicized_ **bold** list item with `code` inline.
Another item with **nested** inline **markup**.
This list item uses some `inline code` and ends with _**italicized and bold**_ text.
To write code, you can use backticks for `inline code`, like this."""

MD = """**Markdown Example** with _**Inline Markup**_. 
This is a **bold** statement, and this is an _italicized_ one. 
You can even combine them to make text _**both italic and bold**_. 
This item has some inline markup like _italics_ and **bold** text. 
Even deeper nesting: _Italicized_ **bold** list item with `code` inline. 
Another item with **nested** inline **markup**. 
This list item uses some ``inline sample codee`` and ends with _**italicized and bold**_ text. 
To write code, you can use backticks for `inline code`, like this."""

#MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "

MD = "This is some **markdown *where we have* double *nested italics * which** might be confusing"

TOKENIZER_LIST = "(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)"
TOKENIZER_LIST = "(?P<tick>`{1,2})|(?P<asterisk>\*{1,2})|(?P<underscore>_{1,3})|(?P<tilde>~{1,2})|(?P<dash>-{1,2})|(?P<assign>={1,2})|(?P<colon>:{1})|(?P<caret>\^{1})|(?P<dollar>\${1})|(?P<less><{1})|(?P<text>\w+)"
TOKENIZER_LIST = "(?P<asterisk2>\*{2})|(?P<asterisk1>\*{1})|(?P<text>\w+)"
TOKENIZER_LIST = "(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)|(?P<text> ?\w+ ?)"
TOKENIZER_LIST = "(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)|(?P<text>.| )"
TOKENIZER_LIST = "(?P<samp>``)|(?P<strong>(?:\*\*)|(?:__))|(?P<del>(?:~~)|(?:--))|(?P<mark>==)|(?P<em>(?:\*)|(?:_))|(?P<code>`)|(?P<sup>\^)|(?P<sub>~)|(?P<math>\$)|(?P<emoji>\:)|(?P<text>.)"

TOKENIZER = re.compile(TOKENIZER_LIST)

BTRACKER = {
    "asterisk2": False,
    "asterisk1": False,
}


mdtokens = md_string_tokenizer(TOKENIZER, MD)    
BTRACKER = create_tracker_from_tokenizer(TOKENIZER)
converted = parse_inline_tokens(mdtokens, BTRACKER)

#print(converted)
print(json.dumps(converted, indent=4))

# %%
