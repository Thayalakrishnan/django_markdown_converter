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
    ("samp", ("``",)),
    ("strong", ("\*\*", "__",)),
    ("del", ("~~", "--",)),
    ("mark", ("==",)),
    ("em", ("\*", "_",)),
    ("code", ("`",)),
    ("sup", ("\^",)),
    ("sub", ("~",)),
    
    #("math", ("\$",)),
    #("emoji", ("\:",)),
    
    ("math", ("(?:\$)([^\$]+?)(?:\$)",)),
    ("emoji", ("(?:\:)(.+?)(?:\:)",)),
    ("footnote", ("(?:\[\^)(\d+?)(?:\])",)),
    ("text", (".",)),
    #("link", ("\<", "\>",)),
    #("link", ("\[", "\)",)),
]

"""
just added the footnote by doing the whole pattern
this feels like a much better algo then we had before

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
"""

def create_patterns_for_tokenizer(tokens:list=[]) -> str:
    pattern_list = []
    for label, pats in tokens:
        if len(pats) > 1:
            patterns = "|".join([f"(?:{_})" for _ in pats])
        else:
            patterns = f"{pats[0]}"
        labelled_pattern = f"(?P<{label}>{patterns})"
        pattern_list.append(labelled_pattern)
    return "|".join(pattern_list)


#%%
import re

"""
we can solve a lot of heart ache by having a check function for each pattern 
to ensure that we can look ahead in the same string and determine an end point
"""

def md_string_tokenizer(pattern, source):
    matches = pattern.finditer(source)
    current_text_group = []

    for match in matches:
        token = match.lastgroup
        content = match.group(token)
        
        if token == "text":
            current_text_group.append(content)
        #elif token == "footnote":
        #    yield ("text", "".join(current_text_group))
        #    yield ("footnote", content)
        else:
            
            if len(current_text_group):
                # if we are holding some text, we should release it all now
                # this will be all the text from the last token to the curren 
                # token
                yield ("text", "".join(current_text_group))
                current_text_group = []
            # yield the current token
            yield (token, content)
    ## yield any remaining text
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
    bank = []
    root = {"type": "root", "data": []}
    current_object = root

    for token, value in tokens:
        
        #if token == "footnote":
        #    current_object["data"].append({"type": token, "data": value})
        if token not in ["text", "footnote", "emoji", "math"]:
            # flip the switch
            tracker[token] = not tracker[token]
            
            # if the token is open
            if tracker[token]:
                # new open token, increase the depth
                depth+=1
                # create a new object
                new_object = {"type": "", "data": []}
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
                        # if there is only one child element, just make that one child
                        # equal to it
                        if len(current_object["data"]) == 1:
                            single_child = current_object["data"].pop()
                            if single_child["type"] == "text":
                                current_object["data"] = single_child["data"]
                            else:
                                current_object["data"] = single_child
                        current_object = object_stack.pop()
                depth-=1
        else:
            current_object["data"].append({"type": token, "data": value})
    # we need to check that we have returned to a depth of zero. 
    # if we have not, whatever is preventing it needs to be removed
    #if depth:
    #    root_object = object_stack.pop()
    #    previous_object = root_object["data"].pop()
    #    root_object["data"].extend(previous_object["data"])
    return root["data"]


# %%
def parse_inline_tokens(tokens, tracker):
    depth = 0
    object_stack = []
    bank = []
    root = ("root", [])
    current_object = root

    for token, value in tokens:
        
        if token not in ["text", "footnote", "emoji", "math"]:
            # flip the switch
            tracker[token] = not tracker[token]
            # if the token is open
            if tracker[token]:
                # new open token, increase the depth
                depth+=1
                # create a new object
                new_object = ["", []]
                # add the new object as a child to the current object
                current_object[1].append(new_object)
                # add the current object to the stack
                object_stack.append(current_object)
                # assign the new object as the current object
                current_object = new_object
            else:
                # if the token is closed
                if depth:
                    if len(object_stack):
                        current_object[0] = token
                        # if there is only one child element, just make that one child
                        # equal to it
                        if len(current_object[1]) == 1:
                            single_child = current_object[1].pop()
                            if single_child[0] == "text":
                                current_object[1] = single_child[1]
                            else:
                                current_object[1] = single_child
                        current_object = object_stack.pop()
                depth-=1
        else:
            current_object[1].append([token, value])
    return root[1]

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

MD = """Before **middle content** after. 
Before __middle content__ after. 
Before _middle content_ after. 
Before *middle content* after. 
Before ^middle content^ after. 
Before ~middle content~ after. 
Before ~~middle content~~ after. 
Before ==middle content== after. 
Before --middle content-- after. 
Before :middle_content: after. 
Before `middleContent` after. 
Before ``middleContent`` after. 
Before [link to Markdown documentation](https://www.markdownguide.org) after. 
Before <https://www.markdownguide.org> after. 
Before [^1] after. """

#MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "
#MD = "This is some **markdown *where we have* double *nested italics * which** might be confusing"

TOKENIZER_LIST = create_patterns_for_tokenizer(TOKENS)
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
