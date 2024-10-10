# %%
import re, json

class ScannerGenerator(re.Scanner):
    def scan(self, string):
        tracker = {
            "strong": False,
            "del": False,
            "mark": False,
            "sup": False,
            "sub": False,
            "em": False,
            "samp": False,
            "code": False,
        }
        text_group = ""
        match = self.scanner.scanner(string).match
        i = 0
        depth = 0
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
                # (token, value, nestable)
                self.match = m
                ret = action(m.group())
                token, value, is_nestable = ret
                
                if token == "text":
                    text_group+=value
                else:
                    if is_nestable:
                        tracker[token] = not tracker[token]
                    if tracker[token]:
                        depth+=1
                    else:
                        depth-=1
                        
                    if len(text_group):
                        yield ("text", text_group, False, False, depth)
                        text_group = ""
                    yield (token, value, is_nestable, tracker[token], depth)
            # set i to j so we know
            # we are moving along the string
            i = j
        text_group+=string[i:]
        yield ("text", text_group, False, False, depth)

"""
the lambda receive the value of the token
the lambda should return, in order
label, token value, if the token can be nested
"""
scanner = ScannerGenerator([
    (r"(?:\*\*)|(?:__)", lambda t: ["strong", t, True]),
    (r"(?:\~\~)|(?:\-\-)", lambda t: ["del", t, True]),
    (r"\=\=", lambda t: ["mark", t, True]),
    (r"\^(?=[^\^])", lambda t: ["sup", t, True]),
    (r"\~(?=[^\~])", lambda t: ["sub", t, True]),
    (r"(?:\*)|(?:_)", lambda t: ["em", t, True]),
    (r"``", lambda t: ["samp", t, True]),
    (r"`", lambda t: ["code", t, True]),
    
    (r"\$.*?\$", lambda t: ["math", t, False]),
    (r"\:.*?\:", lambda t: ["emoji", t[1:-1], False]),
    (r"\[\^\d+\]", lambda t: ["footnote", t[2:-1], False]),
    (r"\[.*?\]\([^ ]+?\)", lambda t: ["link", t, False]),
    
    (r"\<(\S+)[^\>\<]*?\>.*?\<\/\1\>", lambda t: ["html", t, False]),
    (r"\<[^ ]+?\>", lambda t: ["rawlink", t[1:-1], False]),
    #(r"\w+", lambda t: ["text", t, True]),
    (r"[a-zA-Z0-9]+", lambda t: ["text", t, False]),
    (r"\s+", lambda t: ["text", t, False]),
    (r".+?", lambda t: ["text", t, False]),
])


MD_TEST_CASES = [
    ## regular
    ("**formatted content**", ["strong", "formatted content"]),
    #("before **in between** after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    #("before __in between__ after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    #("before _in between_ after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    #("before *in between* after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    #("before ^in between^ after", [["text", "before "], ["sup", "in between"], ["text", " after"]]),
    #("before ~in between~ after", [["text", "before "], ["sub", "in between"], ["text", " after"]]),
    #("before ~~in between~~ after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    #("before --in between-- after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    #("before ==in between== after", [["text", "before "], ["mark", "in between"], ["text", " after"]]),
    #("before ``in between`` after", [["text", "before "], ["samp", "in between"], ["text", " after"]]),
    #("before :in between: after", [["text", "before "], ["emoji", "in between"], ["text", " after"]]),
    #("before `in between` after", [["text", "before "], ["code", "in between"], ["text", " after"]]),
    #("before <https://in.between.org> after", [["text", "before "], ["rawlink", "https://in.between.org"], ["text", " after"]]),
    #("before [^1] after", [["text", "before "], ["footnote", "1"], ["text", " after"]]),
    #("before [in between](https://in.between.org) after", [["text", "before "], ["link", "[in between](https://in.between.org)"], ["text", " after"]]),
    #("before <navlink title=\"in between\">in between</navlink> after", [["text", "before "], ["html", "<navlink title=\"in between\">in between</navlink>"], ["text", " after"]]),
    #
    ### single nesting
    #("before **in `nested content` between** after", [["text", "before "], ["strong", [["text", "in "], ["code", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ### double nesting
    #("before **in _nested `double nested` content_ between** after", [["text", "before "], ["strong", [["text", "in "], ["em", [["text", "nested "], ["code", "double nested"], ["text", " content"]]], ["text", " between"]]], ["text", " after"]]),
    ### order of operations
    #("before ==in **nested content** between== after", [["text", "before "], ["mark", [["text", "in "], ["strong", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ### unbalanced
    #("before **unbalanced _nested `content`**", [["text", "before "], ["strong", [["text", "unbalanced nested "], ["code", "content"]]]]),
    ### irregular nesting
    #("before **in `nested content between** after", [["text", "before "], ["strong", "in nested content between"], ["text", " after"]]),
    ### edge cases
    #("How about some **strong _emphasised --deleted ^super ==marked ~sub content as well", "How about some strong emphasised deleted super marked sub content as well"),
    ### long and complex
    (
        "**Markdown Example** with _**Inline Markup**_. This **_==`inline code`==_** and ends with _**italicized and bold**_ text. Some __super *nested ==deep content `right here`== right now* duper__ yeet. Going ~~in *and in* and out *and then in again* and then out~~ yeet.", 
        [['strong', 'Markdown Example'],['text', ' with '],['em', ['strong', 'Inline Markup']],['text', '. This '],['strong', ['em', ['mark', ['code', 'inline code']]]],['text', ' and ends with '],['em', ['strong', 'italicized and bold']],['text', ' text. Some '],['strong', [['text', 'super '],['em', [['text', 'nested '],['mark', [['text', 'deep content '],['code', 'right here']]],['text', ' right now']]],['text', ' duper']]],['text', ' yeet. Going '],['del', [['text', 'in '],['em', 'and in'],['text', ' and out '],['em', 'and then in again'],['text', ' and then out']]],['text', ' yeet.']]
    ),
]


for index, case in enumerate(MD_TEST_CASES):
    md, solution = case
    print(f"case {index} ---------- {md}")
    tokens = scanner.scan(md)
    for _ in tokens:
        print(_)

            
# %%
