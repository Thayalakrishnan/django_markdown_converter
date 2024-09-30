import pytest
from django_markdown_converter.patterns.inlines.parser import convert_inline, revert_inline



INLINE_BLOCK_DATA_SMALL = [
    {
        "tag": "text",
        "data": "Example sentence with some "
    },
    {
        "tag": "strong",
        "data": "bolded text"
    },
    {
        "tag": "text",
        "data": " and a footnote"
    },
    {
        "tag": "footnote",
        "data": "1"
    },
    {
        "tag": "text",
        "data": " to boot."
    }
]

INLINE_MD_DATA_SMALL = "Example sentence with some **bolded text** and a footnote[^1] to boot."

def test_basic_conversion():
    """
    """
    result = convert_inline(INLINE_MD_DATA_SMALL)
    print(result)
    assert INLINE_BLOCK_DATA_SMALL == result


def test_basic_reversion():
    """
    """
    result = revert_inline(INLINE_BLOCK_DATA_SMALL)
    print(repr(result))
    assert INLINE_MD_DATA_SMALL == result



INLINE_TEST_DATA_BEFORE = {"tag": "text", "data": "before "}
INLINE_TEST_DATA_AFTER = {"tag": "text", "data": " after"}

INLINE_TEST_DATA = [
    # code
    ("before `middle` after", [INLINE_TEST_DATA_BEFORE, {"tag": "code", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # strong
    ("before **middle** after", [INLINE_TEST_DATA_BEFORE, {"tag": "strong", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # em
    ("before _middle_ after", [INLINE_TEST_DATA_BEFORE, {"tag": "em", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # del
    ("before --middle-- after", [INLINE_TEST_DATA_BEFORE, {"tag": "del", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # mark
    ("before ==middle== after", [INLINE_TEST_DATA_BEFORE, {"tag": "mark", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # emoji
    ("before :middle: after", [INLINE_TEST_DATA_BEFORE, {"tag": "emoji", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # sup
    ("before ^middle^ after", [INLINE_TEST_DATA_BEFORE, {"tag": "sup", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # sub
    ("before ~middle~ after", [INLINE_TEST_DATA_BEFORE, {"tag": "sub", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # math
    ("before $middle$ after", [INLINE_TEST_DATA_BEFORE, {"tag": "math", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # link
    ("before [title](src) after", [INLINE_TEST_DATA_BEFORE, {"tag": "link", "data": {"to": "src", "title": "title"}}, INLINE_TEST_DATA_AFTER]),
    # footnote
    ("before [^1] after", [INLINE_TEST_DATA_BEFORE, {"tag": "footnote", "data": "1"}, INLINE_TEST_DATA_AFTER]),
    # samp
    ("before ``middle`` after", [INLINE_TEST_DATA_BEFORE, {"tag": "samp", "data": "middle"}, INLINE_TEST_DATA_AFTER]),
    # email
]


def test_basic_conversion_loop():
    """
    """
    for md, solution in INLINE_TEST_DATA:
        result = convert_inline(md)
        print(result)
        assert solution == result



def test_basic_reversion_loop():
    """
    """
    for solution, blocks in INLINE_TEST_DATA:
        result = revert_inline(blocks)
        print(result)
        assert solution == result
        

## bigger blocks

INLINE_BLOCK_DATA_BIG = [
    {
        "tag": "text",
        "data": "Example sentence with some "
    },
    {
        "tag": "strong",
        "data": "bolded text"
    },
    {
        "tag": "text",
        "data": " and a footnote"
    },
    {
        "tag": "footnote",
        "data": "1"
    },
    {
        "tag": "text",
        "data": " to boot. "
    },
    {
        "tag": "mark",
        "data": "This part is highlighted"
    },
    {
        "tag": "text",
        "data": " which makes it stand out from other content like "
    },
    {
        "tag": "code",
        "data": "inline code"
    },
    {
        "tag": "text",
        "data": " and "
    },
    {
        "tag": "em",
        "data": "italicised words"
    },
    {
        "tag": "text",
        "data": ". We can even make sure that some content "
    },
    {
        "tag": "sup",
        "data": "is above"
    },
    {
        "tag": "text",
        "data": " and some "
    },    
    {
        "tag": "sub",
        "data": "is below"
    },
    {
        "tag": "text",
        "data": " and some is simply "
    },
    {
        "tag": "del",
        "data": "deleted"
    },
    {
        "tag": "text",
        "data": ". This is some math "
    },
    {
        "tag": "math",
        "data": "y=mx+b"
    },
    {
        "tag": "text",
        "data": " and this is an "
    },
    {
        "tag": "emoji",
        "data": "emoji"
    },
    {
        "tag": "text",
        "data": " along with some "
    },
    {
        "tag": "code",
        "data": "output"
    },
    #{
    #    "tag": "text",
    #    "data": "."
    #},
    {
        "tag": "text",
        "data": ". Here's a "
    },
    {
        "tag": "link",
        "data": {
            "to": "www.markdownguide.org",
            "title": "link to Markdown documentation"
        }
    },
    {
        "tag": "text",
        "data": "."
    },
]



INLINE_MD_DATA_BIG = [
    "Example sentence with some **bolded text** and a footnote[^1] to boot.",
    "==This part is highlighted== which makes it stand out from other content like `inline code` and _italicised words_.",
    "We can even make sure that some content ^is above^ and some ~is below~ and some is simply --deleted--.",
    "This is some math $y=mx+b$ and this is an :emoji: along with some `output`.",
    "Here's a [link to Markdown documentation](www.markdownguide.org).",
]

INLINE_MD_DATA_BIG = " ".join(INLINE_MD_DATA_BIG)


def test_basic_conversion_bigblock():
    """
    """
    result = convert_inline(INLINE_MD_DATA_BIG)
    for _ in result:
        print(_)
    assert INLINE_BLOCK_DATA_BIG == result


def test_basic_reversion_bigblock():
    """
    """
    result = revert_inline(INLINE_BLOCK_DATA_BIG)
    print(repr(INLINE_MD_DATA_BIG))
    print(repr(result))
    assert INLINE_MD_DATA_BIG == result