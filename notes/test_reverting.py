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
BLOCK = {
    'type': 'ulist',
    'data': [
        {
            'type': 'item',
            'data': [
                'Item 1: line 1.\n'
            ]
        },
        {
            'type': 'item',
            'data': [
                'Item 2: line 1.\n', 
                {
                    'type': 'ulist',
                    'data': [
                        {
                            'type': 'item',
                            'data': [
                                'Item 2.1: line 1.\n', 
                                {
                                'type': 'ulist',
                                'data': [
                                    {
                                    'type': 'item',
                                    'data': ['Item 2.1.1: line 1.\n']
                                }]
                            }]
                        },
                {
                    'type': 'item',
                    'data': ['Item 2.2: line 1.\n']
                }]
            }]
        },
    {
        'type': 'item',
        'data': ['Item 3: line 1.\n', {
            'type': 'ulist',
            'data': [{
                'type': 'item',
                'data': ['Item 3.1: line 1.\n', {
                    'type': 'ulist',
                    'data': [{
                        'type': 'item',
                        'data': ['Item 3.1.1: line 1.\n']
                    }]
                }]
            },
            {
                'type': 'item',
                'data': ['Item 3.2: line 1.\n']
            }]
        }]
    },
    {
        'type': 'item',
        'data': ['Item 4: line 1.\n']
    }]
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

BLOCK = {
    'type': 'ulist',
    'data': [
        {
            'type': 'item',
            'data': [
                'Item 1: line 1.\n'
            ]
        },
        {
            'type': 'item',
            'data': [
                'Item 2: line 1.\n'
            ]
        },
        {
            'type': 'item',
            'data': [
                'Item 3: line 1.\n'
            ]
        },
        {
            'type': 'item',
            'data': [
                'Item 4: line 1.\n'
            ]
        },
        {
            'type': 'item',
            'data': [
                'Item 5: line 1.\n'
            ]
        },
    ]
}



#%%
"""
the functions after removing "children" from the list object
"""


def Flatten(block:dict={}, level:int=0, shared_arr:list=[]):
    #print(f"level: {level}")
    blocklist = block["data"]
    for block in blocklist:
        for subblock in block["data"]:
            """
            if a subblock is a block (dict) we need to convert it
            back to string form
            if its a list block (either olist or ulist), we can flatten the list
            right here
            if its not a list block, we need to convert the block to a string appropriately
            """
            if isinstance(subblock, dict):
                if subblock["type"] == "olist" or subblock["type"] == "ulist":
                    subblock = Flatten(subblock, level+2, shared_arr)
                #else:
                #    subblock = 
            if isinstance(subblock, str):
                shared_arr.append(f"{level*' '}- {subblock}")
    

def Revert(block:dict={}):
    myarr = []
    Flatten(block, 0, myarr)
    return "".join(myarr)


print(Revert(BLOCK))
# %%
