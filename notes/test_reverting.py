#%%
BLOCK = {
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
                    "data": "Item 1"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 2"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 3"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 4"
                }
            ]
        }
    ]
}

BLOCK = {
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
                    "data": "Item 1"
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 2"
                }
            ]
        },
        {
            "type": "ulist",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 3"
                }
            ],
            "children": [
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Indented Item 1"
                        }
                    ]
                },
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Indented Item 2"
                        }
                    ]
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 4"
                }
            ]
        }
    ]
}

#%%

BLOCK = {
    "type": "ulist",
    "data": [
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 1: line 1.\nItem 1: line 2."
                }
            ]
        },
        {
            "type": "ulist",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 2: line 1.\nItem 2: line 2."
                },
                {
                    "type": "paragraph",
                    "data": "Item 2: line 3."
                }
            ],
            "children": [
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 2.1: line 1."
                        }
                    ]
                },
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 2.2: line 1."
                        }
                    ]
                },
                {
                    "type": "olist",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 2.3: line 1."
                        }
                    ],
                    "children": [
                        {
                            "type": "item",
                            "data": [
                                {
                                    "type": "paragraph",
                                    "data": "Item 2.3.1: line 1."
                                }
                            ]
                        },
                        {
                            "type": "item",
                            "data": [
                                {
                                    "type": "paragraph",
                                    "data": "Item 2.3.2: line 1."
                                }
                            ]
                        },
                        {
                            "type": "item",
                            "data": [
                                {
                                    "type": "paragraph",
                                    "data": "Item 2.3.3: line 1."
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 2.4: line 1."
                        }
                    ]
                }
            ]
        },
        {
            "type": "ulist",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 3: line 1."
                }
            ],
            "children": [
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 3.1: line 1.\nItem 3.1: line 2."
                        },
                        {
                            "type": "code",
                            "props": {
                                "language": "python"
                            },
                            "data": []
                        },
                        {
                            "type": "paragraph",
                            "data": "Item 3.1: line 3."
                        }
                    ]
                },
                {
                    "type": "item",
                    "data": [
                        {
                            "type": "paragraph",
                            "data": "Item 3.2: line 1."
                        }
                    ]
                }
            ]
        },
        {
            "type": "item",
            "data": [
                {
                    "type": "paragraph",
                    "data": "Item 4: line 1."
                }
            ]
        }
    ]
}

#%%
def TraverseList(blocklist:list=[]):
    for block in blocklist:
        if isinstance(block["data"], list):
            FlattenList(block["data"])
            if "children" in block:
                FlattenList(block["children"])
        if isinstance(block["data"], str):
            print(block["data"])
    return


def FlattenList(blocklist:list=[]):
    for block in blocklist:
        if isinstance(block["data"], list):
            print(f"blocktype: {block['type']}")
            if "children" in block:
                block["data"].extend(block["children"])
                del block["children"]
                #FlattenList(block["children"])
                
            print(f"blocktype: {block['type']}")
            if block["type"]=="item":
                FlattenList(block["data"])
            
        if isinstance(block["data"], str):
            #print(block["data"])
            pass
    return


#for b in BLOCK["data"]:
#    print(b)
    
TraverseList(BLOCK["data"])
print("traversal done")

FlattenList(BLOCK["data"])
print("flatten done")

TraverseList(BLOCK["data"])
print("traversal done")

print("done")
# %%
