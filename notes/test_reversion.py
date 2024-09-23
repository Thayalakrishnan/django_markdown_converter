from django_markdown_converter.revert import Revert
from django_markdown_converter.patterns.blocks.paragraph import ParagraphPattern
from django_markdown_converter.patterns.blocks.list import ListPattern
from django_markdown_converter.patterns.lookups import PARAGRAPH_PATTERN, ULIST_PATTERN

BLOCKS = [
    {
        "type": "heading",
        "props": {
            "blocktype": "heading",
            "level": 2
        },
        "data": "Ordered List"
    },
    {
        "type": "paragraph",
        "props": {},
        "data": "Item 4"
    }
]


#print(Revert(BLOCKS))


PBLOCK = {
    "type": "paragraph",
    "props": {
        "blocktype": "paragraph"
    },
    "data": [
        {
            "tag": "text",
            "data": "Pargraph 4 "
        },
        {
            "tag": "strong",
            "data": "eos"
        },
        {
            "tag": "text",
            "data": " aperiam dolorem numquam quisquam "
        },
        {
            "tag": "footnote",
            "data": "1"
        },
        {
            "tag": "text",
            "data": ". Cupiditate "
        },
        {
            "tag": "mark",
            "data": "reprehenderit"
        },
        {
            "tag": "text",
            "data": " beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus "
        },
        {
            "tag": "code",
            "data": "code"
        },
        {
            "tag": "text",
            "data": " voluptates "
        },
        {
            "tag": "em",
            "data": "similique"
        },
        {
            "tag": "text",
            "data": ". Aut maiores hic laudantium distinctio"
        },
        {
            "tag": "footnote",
            "data": "2"
        },
        {
            "tag": "text",
            "data": ". Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit"
        },
        {
            "tag": "sup",
            "data": "5"
        },
        {
            "tag": "text",
            "data": " ex aspernatur eius "
        },
        {
            "tag": "del",
            "data": "consectetur"
        },
        {
            "tag": "text",
            "data": " blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in."
        }
    ]
}


PBLOCK_NESTED = {
    "type": "paragraph",
    "props": {
        "blocktype": "paragraph"
    },
    "data": [
        {
            "tag": "text",
            "data": "Before nested part. "
        },
        {
            "tag": "strong",
            "data": [
                {
                    "tag": "text",
                    "data": "First part of nested bit. "
                },
                {
                    "tag": "mark",
                    "data": "Marked part of nested bit "
                },
                {
                    "tag": "footnote",
                    "data": "1"
                },
                {
                    "tag": "text",
                    "data": " After the footnote in the nested bit."
                },
            ]
        },
        {
            "tag": "text",
            "data": " After nested part. "
        },
    ]
}


#print(ParagraphPattern(PARAGRAPH_PATTERN).revert(PBLOCK_NESTED))


LBLOCK = {
    "type": "ulist",
    "props": {
        "blocktype": "u list"
    },
    "data": [
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "props": {},
                    "data": "Item 1"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "props": {},
                    "data": "Item 2"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "props": {},
                    "data": "Item 3"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "props": {},
                    "data": "Item 4"
                }
            ]
        }
    ]
}

LBLOCK = """- Item 1: line 1.
- Item 2: line 1.
    - Item 2.1: line 1.
        - Item 2.1.1: line 1.
    - Item 2.2: line 1.
- Item 3: line 1.
    - Item 3.1: line 1.
        - Item 3.1.1: line 1.
    - Item 3.2: line 1.
- Item 4: line 1.
"""


converted = ListPattern(ULIST_PATTERN).convert(LBLOCK)

print(converted)


