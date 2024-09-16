import re
from django_markdown_converter.patterns.classes.base import BasePattern

class ListPattern(BasePattern):
    """
    olist, ulist
    """
    def get_match(self, content):
        self.match = ConvertListIntoItems(content)
    
    def get_data(self) -> dict:
        return ConvertList(self.match, self.bank)
    
    def update_props(self):
        pass


def FormatContent(fresh:str="") -> str:
    fresh = fresh.strip().split("\n")
    fresh = [_.lstrip() for _ in fresh]
    return "\n".join(fresh)

def FormatItem(yeet:dict=()):
    yeet["type"] = "item"
    yeet["level"] = len(yeet["level"])
    yeet["marker"] = "ulist" if yeet["marker"] == "- " else "olist"
    yeet["children"] = None
    yeet["data"] = FormatContent(yeet["data"])
    return yeet


def ConvertListIntoItems(source:str=""):
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<data>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    return lineitempattern.finditer(source)

def AddItemToList(parent, child):
    del child["marker"]
    del child["level"]
    parent.append(child)


def ConvertList(items, bank):
    """
    """
    stack = []
    
    root = {
        "level": -2, 
        "type": "root", 
        "props": {}, 
        "children": None
    }
    cur_parent = {"children": [root]}
    cur_lvl = -2
    
    for next_item in items:
        item = FormatItem(next_item.groupdict())
        bank.append(item)
        
        while True:
        
            if item["level"] < cur_lvl:
                cur_parent, cur_lvl = stack.pop()
            elif item["level"] > cur_lvl:
                """
                if the current items level is bigger than the 
                the current level, it is nested under the current item
                """
                stack.append((cur_parent, cur_lvl))
                cur_lvl = item["level"]
                cur_parent = cur_parent["children"][-1]
                
                # if there are no current children, add a list
                if not cur_parent["children"]:
                    cur_parent["type"] = item["marker"]
                    cur_parent["children"] = []
            else:
                AddItemToList(cur_parent["children"], item)
                break
    del root["level"]
    for _ in bank:
        if "children" in _ and not _["children"]:
            del _["children"]
    return root["children"]
