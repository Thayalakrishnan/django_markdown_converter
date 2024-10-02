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
import re

MD_LIST = [
    "Before **middle content** after.",
    "Before __middle content__ after.",
    "Before _middle content_ after.",
    "Before *middle content* after.",
    "Before ^middle content^ after.",
    "Before ~middle content~ after.",
    "Before ~~middle content~~ after.",
    "Before --middle content-- after.",
    "Before ==middle content== after.",
    "Before ``middleContent`` after.",
    "Before :middle_content: after.",
    "Before `middleContent` after.",
    "Before <https://www.markdownguide.org> after.",
    "Before [^1] after.",
    "Before [link to Markdown documentation](https://www.markdownguide.org) after.",
]


class ScannerGenerator(re.Scanner):
    def scan(self, string):
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
                self.match = m
                action = action(self, m.group())
            if action is not None:
                yield action
            # set i to j so we know 
            # we are moving along the string
            i = j
        yield ['text', string[i:]]
    

scanner = ScannerGenerator([
    (r"\*\*", lambda s,t: ["strong", t]),
    (r"__", lambda s,t: ["strong", t]),
    (r"\~\~", lambda s,t: ["del", t]),
    (r"\=\=", lambda s,t: ["mark", t]),
    (r"\-\-", lambda s,t: ["del", t]),
    (r"``.+?``", lambda s,t: ["samp", t[2:-2]]),
    (r"\^(?=[^\^])", lambda s,t: ["sup", t]),
    (r"\~(?=[^\~])", lambda s,t: ["sub", t]),
    (r"\`.+?\`", lambda s,t: ["code", t[1:-1]]),
    (r"\*", lambda s,t: ["em", t]),
    (r"_", lambda s,t: ["em", t]),
    
    (r"\$.*?\$", lambda s,t: ["math", t]),
    (r"\:.*?\:", lambda s,t: ["emoji", t[1:-1]]),
    (r"\[\^\d+\]", lambda s,t: ["footnote", t[2:-1]]),
    (r"\[.*?\]\([^ ]+?\)", lambda s,t: ["link", t]),
    (r"\<[^ ]+?\>", lambda s,t: ["rawlink", t[1:-1]]),
    (r"\<\s+[^ ]+?\>", lambda s,t: ["html", t[1:-1]]),
    
    (r"[a-zA-Z0-9]+", lambda s,t: ["text", t]),
    #(r"\w+", lambda s,t: ["text", t]),
    (r"\s+", lambda s,t: ["text", t]),
    (r".+?", lambda s,t: ["text", t]),
])


#for _ in MD_LIST:
#    
#    tokens, remainder = scanner.scan(_)
#    
#    for _ in tokens:
#        if _[0] != "text":
#            print(_)
#    print(remainder)


MD = " ".join(MD_LIST)
tokens = scanner.scan(MD)
for _ in tokens:
    print(_)

# %%
