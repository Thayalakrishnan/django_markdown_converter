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

    def revert(self, *args, **kwargs) -> str:
        """
        if the blocktype is list we need to ensure that all the list items
        we can only really handle the nested list items or any list when the structure is flatenned.
        """
        super().revert(*args, **kwargs)

        blocktype = self.block.get("type", "ulist")
        props = self.block.get("props", {})
        data = self.block.get("data", "")

        ret = []

        """
        when we flatten a list we want to go from having a list of blocks to a list of strings
        """
        # traverse the list and merge all the children into data
        if "children" in self.block:
            if isinstance(data, list):
                self.block["data"].extend(self.block["chldren"])
                del self.block["children"]

        if isinstance(data, list):
            return

        ## check that all the data is type str before converting it all
        for _ in self.block["data"]:
            if not isinstance(_["data"], str):
                break

        for index, _ in enumerate(data):
            if _["type"] == "item":
                if blocktype == "ulist":
                    ret.append(f"- {_["data"]}")
                else:
                    ret.append(f"{index}. {_}")

        ret.append("")
        return "\n".join(ret)




def FormatItem(yeet:dict=()):
    """
    TODO: use the level to set the amount of padding to remove
    from each line. it should be level + 1 i think, depending on
    type of list maybe
    """
    level = len(yeet["level"])
    padding = level + len(yeet["marker"])
    data = yeet["data"]
    data = re.sub(pattern=f'^ {{{padding}}}', repl='', string=data, flags=re.MULTILINE)
    return {
        "type": "item",
        "level": level,
        "marker": "ulist" if yeet["marker"] == "- " else "olist",
        "data": data,
        "children": None,
    }


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
