# %%
from proto.parser import parse

MD_TEST_CASES = [
    ## regular
    ("**formatted content**", ["strong", "formatted content"]),
    ("before **in between** after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    ("before __in between__ after", [["text", "before "], ["strong", "in between"], ["text", " after"]]),
    ("before _in between_ after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    ("before *in between* after", [["text", "before "], ["em", "in between"], ["text", " after"]]),
    ("before ^in between^ after", [["text", "before "], ["sup", "in between"], ["text", " after"]]),
    ("before ~in between~ after", [["text", "before "], ["sub", "in between"], ["text", " after"]]),
    ("before ~~in between~~ after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    ("before --in between-- after", [["text", "before "], ["del", "in between"], ["text", " after"]]),
    ("before ==in between== after", [["text", "before "], ["mark", "in between"], ["text", " after"]]),
    ("before ``in between`` after", [["text", "before "], ["samp", "in between"], ["text", " after"]]),
    ("before :in between: after", [["text", "before "], ["emoji", "in between"], ["text", " after"]]),
    ("before `in between` after", [["text", "before "], ["code", "in between"], ["text", " after"]]),
    ("before <https://in.between.org> after", [["text", "before "], ["rawlink", "https://in.between.org"], ["text", " after"]]),
    ("before [^1] after", [["text", "before "], ["footnote", "1"], ["text", " after"]]),
    ("before [in between](https://in.between.org) after", [["text", "before "], ["link", "[in between](https://in.between.org)"], ["text", " after"]]),
    ("before <navlink title=\"in between\">in between</navlink> after", [["text", "before "], ["html", "<navlink title=\"in between\">in between</navlink>"], ["text", " after"]]),
    
    ## single nesting
    ("before **in `nested content` between** after", [["text", "before "], ["strong", [["text", "in "], ["code", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ## double nesting
    ("before **in _nested `double nested` content_ between** after", [["text", "before "], ["strong", [["text", "in "], ["em", [["text", "nested "], ["code", "double nested"], ["text", " content"]]], ["text", " between"]]], ["text", " after"]]),
    ## order of operations
    ("before ==in **nested content** between== after", [["text", "before "], ["mark", [["text", "in "], ["strong", "nested content"], ["text", " between"]]], ["text", " after"]]),
    ## unbalanced
    ("before **unbalanced _nested `content`**", [["text", "before "], ["strong", [["text", "unbalanced nested "], ["code", "content"]]]]),
    ## irregular nesting
    ("before **in `nested content between** after", [["text", "before "], ["strong", "in nested content between"], ["text", " after"]]),
    ## edge cases
    ("How about some **strong _emphasised --deleted ^super ==marked ~sub content as well", "How about some strong emphasised deleted super marked sub content as well"),
    ## long and complex
    (
        "**Markdown Example** with _**Inline Markup**_. This **_==`inline code`==_** and ends with _**italicized and bold**_ text. Some __super *nested ==deep content `right here`== right now* duper__ yeet. Going ~~in *and in* and out *and then in again* and then out~~ yeet.", 
        [['strong', 'Markdown Example'],['text', ' with '],['em', ['strong', 'Inline Markup']],['text', '. This '],['strong', ['em', ['mark', ['code', 'inline code']]]],['text', ' and ends with '],['em', ['strong', 'italicized and bold']],['text', ' text. Some '],['strong', [['text', 'super '],['em', [['text', 'nested '],['mark', [['text', 'deep content '],['code', 'right here']]],['text', ' right now']]],['text', ' duper']]],['text', ' yeet. Going '],['del', [['text', 'in '],['em', 'and in'],['text', ' and out '],['em', 'and then in again'],['text', ' and then out']]],['text', ' yeet.']]
    ),
]


for index, case in enumerate(MD_TEST_CASES):
    md, solution = case
    #print(f"case {index} ---------- {md}")
    answer = parse(md)
    if solution != answer:
        print(f"case {index:{3}} ❌ ---------- {md!r}")
        print(f"failed")
        print("The Solution")
        print(solution)
        print("My Answer")
        print(answer)
    else:
        print(f"case {index:{3}} ✔️ ---------- {md!r}")

#
#MD = """**Markdown Example** with _**Inline Markup**_. This **_==`inline code`==_** and ends with _**italicized and bold**_ text. Some __super *nested ==deep content `right here`== right now* duper__ yeet. Going ~~in *and in* and out *and then in again* and then out~~ yeet."""
#ret = parse(MD)
#print(json.dumps(ret, indent=4))
#print("done ------------------------------")
