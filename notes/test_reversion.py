#%%
from django_markdown_converter.revert import Revert

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


print(Revert(BLOCKS))
# %%
