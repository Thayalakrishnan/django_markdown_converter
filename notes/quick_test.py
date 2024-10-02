from django_markdown_converter.patterns.inlines.parser import convert_inline, revert_inline


MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "


converted = convert_inline(MD)

print(converted)

#%%
import re

pattern = re.compile("(?P<ahead>(?P<code>`)|(?P<strong>\*\*)|(?P<em>\*))(?P<between>(?=.+(?P=ahead)))?")

MD = "***Markdown Example** with* nesting and `inline code` and more *nested italics* at the end."


matches = pattern.finditer(MD)

for _ in matches:
    if _.group("between") is not None:
        print(_.groupdict())
# %%
"""
using re.Scanner
(r"\*\*", lambda s,t: f"Strong({t})"),
(r"\w+", lambda s,t: f"Word({t})"),
(r"\s+", lambda s,t: f"Whitespace({t})"),

(?P<emoji>\:)|

(?P<link>(?:\<)|(?:\>))|
(?P<footnote>(?:\[\^)|(?:\]))|
(?P<link2>(?:\[)|(?:\)))|
"""

MD = "***Markdown Example** with* nesting and `inline code` and more *nested italics* at the end."

MD = """**Markdown Example** with _**Inline Markup**_.
This is a **bold** statement, and this is an _italicized_ one.
You can even combine them to make text _**both italic and bold**_.
This item has some inline markup like _italics_ and **bold** text.
Even deeper nesting: _Italicized_ **bold** list item with `code` inline.
Another item with **nested** inline **markup**.
This list item uses some ``inline sample codee`` and ends with _**italicized and bold**_ text.
To write code, you can use backticks for `inline code`, like this.
This is some **double nested _italicised markdown_ where we nest multiple `different` times** in one line.
Random footnote[^1] near the end."""


# %%
import re, json

MD_LIST = [
    "Before 01 **middle content** after 01.",
    "Before 02 __middle content__ after 02.",
    "Before 03 _middle content_ after 03.",
    "Before 04 *middle content* after 04.",
    "Before 05 ^middle content^ after 05.",
    "Before 06 ~middle content~ after 06.",
    "Before 07 ~~middle content~~ after 07.",
    "Before 08 --middle content-- after 08.",
    "Before 09 ==middle content== after 09.",
    "Before 10 ``middleContent`` after 10.",
    "Before 11 :middle_content: after 11.",
    "Before 12 `middleContent` after 12.",
    "Before 13 <https://www.markdownguide.org> after 13.",
    "Before 14 [^1] after 14.",
    "Before 15 [link to Markdown documentation](https://www.markdownguide.org) after 15.",
    "Before 16 <navlink>middle content</navlink> after 16.",
]

class ScannerGenerator(re.Scanner):
    def scan(self, string):
        text_group = []
        match = self.scanner.scanner(string).match
        i = 0
        while True:
            m = match()
            if not m:
                # no match, break and return string
                break
            j = m.end()
            if i == j:
                # set j to the end of the match
                # if i is equal to j, we have matched
                # at the end again so break
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                #print(action)
                self.match = m
                token, value  = action(m.group())
                if token == "text":
                    text_group.append(value)
                else:
                    yield ["text", "".join(text_group)]
                    text_group = []
                    yield [token, value]
            # set i to j so we know
            # we are moving along the string
            i = j
        text_group.append(string[i:])
        yield ["text", "".join(text_group)]

scanner = ScannerGenerator([
    (r"(?:\*\*)|(?:__)", lambda t: ["strong", t]),
    #(r"\*\*", lambda t: ["strong1", t]),
    #(r"__", lambda t: ["strong2", t]),
    
    (r"(?:\~\~)|(?:\-\-)", lambda t: ["del", t]),
    #(r"\~\~", lambda t: ["del1", t]),
    #(r"\-\-", lambda t: ["del2", t]),
    
    (r"\=\=", lambda t: ["mark", t]),
    (r"``.+?``", lambda t: ["samp", t[2:-2]]),
    (r"\^(?=[^\^])", lambda t: ["sup", t]),
    (r"\~(?=[^\~])", lambda t: ["sub", t]),
    (r"\`.+?\`", lambda t: ["code", t[1:-1]]),
    
    (r"(?:\*)|(?:_)", lambda t: ["em", t]),
    #(r"\*", lambda t: ["em1", t]),
    #(r"_", lambda t: ["em2", t]),

    (r"\$.*?\$", lambda t: ["math", t]),
    (r"\:.*?\:", lambda t: ["emoji", t[1:-1]]),
    (r"\[\^\d+\]", lambda t: ["footnote", t[2:-1]]),
    (r"\[.*?\]\([^ ]+?\)", lambda t: ["link", t]),
    
    (r"\<(\S+)[^\>\<]*?\>.*?\<\/\1\>", lambda t: ["html", t]),
    (r"\<[^ ]+?\>", lambda t: ["rawlink", t[1:-1]]),

    #(r"\w+", lambda t: ["text", t]),
    (r"[a-zA-Z0-9]+", lambda t: ["text", t]),
    (r"\s+", lambda t: ["text", t]),
    (r".+?", lambda t: ["text", t]),
])




# %%
def parse_inline_tokens(tokens):
    depth = 0
    tracker = {}
    object_stack = []
    bank = []
    root = ("root", [])
    current_object = root

    for token, value in tokens:
        
        if token not in ["text", "footnote", "emoji", "math", "link","html", "rawlink"]:
            if token not in tracker:
                tracker[token] = False
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


MD = " ".join(MD_LIST)
tokens = scanner.scan(MD)
for token,value in tokens:
    print(f"{token} | {value}")
#converted = parse_inline_tokens(tokens)
#print(json.dumps(converted, indent=4))
# %%
