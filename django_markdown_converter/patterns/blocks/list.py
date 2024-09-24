import re
from django_markdown_converter.patterns.classes.base import BasePattern
from django_markdown_converter.patterns.data import OLIST_PATTERN, ULIST_PATTERN


class ListPattern(BasePattern):
    """
    olist, ulist
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.item_bank = []
        
    
    def get_match(self, content):
        self.match = ConvertListIntoItems(content)

    def get_data(self) -> dict:
        return self.convert_list(self.match)

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
                    ret.append(f"- {_['data']}")
                else:
                    ret.append(f"{index}. {_}")

        ret.append("")
        return "\n".join(ret)
    
    
    
    def revert(self, *args, **kwargs) -> str:
        super().revert(*args, **kwargs)
        props = self.block.get("props", {})
        ret = []
        self.flatten(self.block, 0, ret)
        return "".join(ret)
    
    def flatten(self, block:dict={}, level:int=0, shared_arr:list=[]):
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
                        subblock = self.flatten(subblock, level+2, shared_arr)
                    else:
                        subblock = self.lookup_revert(block=subblock)

                if isinstance(subblock, str):
                    shared_arr.append(f"{level*' '}- {subblock}")

    def add_to_bank(self, *args, **kwargs) -> None:
        pass

    def create_list_item(self, yeet:dict=()):
        """
        TODO: use the level to set the amount of padding to remove
        from each line. it should be level + 1 i think, depending on
        type of list maybe
        """
        marker = yeet["marker"]
        level = len(yeet["level"])
        padding = level + len(marker)
        # the triple curly braces translates f'^ {{{padding}}}' --> f'^ {4}' for padding = 4
        data = re.sub(pattern=f'^ {{{padding}}}', repl='', string=yeet["data"], flags=re.MULTILINE)
        #data = create_text_item(text)
        #bank.append(data)
        new_item = {
            "type": "item",
            "level": level,
            "marker": DetermineListType(marker),
            "data": self.create_text_item(data),
        }
        self.bank.append(new_item)
        return new_item

    def create_text_item(self, text):
        self.item_bank.append(self.lookup_convert(text))
        return self.item_bank[len(self.item_bank) - 1]
    
    def create_list_block(self, marker):
        return {
            "type": marker,
            "data": [],
        }

    def convert_list(self, items):
        """
        the way nested lists are rendered is by nesting them 
        under an item of the parent list
        our lists are mainly made up of items, lists and text blocks.
        (they are also comprised of other nested block elements)
        
        - to convert our lists, we need to iterate over the items and determine 
        the level of the item
        - if the current item has a larger level then the previous item,
        the current item should be nested under the previous item
        - so we create a new list block based of the current item
        - we then need to grab the previous item and place the new list block
        as as a child under the previous item
        """
        stack = []
        root = {
            "level": 0,
            "type": "root",
            "data": []
        }
        
        cur_parent = root
        cur_lvl = 0

        for item in items:
            current_item = self.create_list_item(item.groupdict())

            while True:
                if current_item["level"] < cur_lvl:
                    cur_parent, cur_lvl = stack.pop()
                elif current_item["level"] > cur_lvl:
                    """
                    if the current items level is bigger than the
                    the current level, it is nested under the current item
                    
                    the stack holds the reference to the parent items
                    note: parent items will only ever reference an item that 
                    can hold nested list items
                    """
                    # add the current level and the current parent to the stack
                    stack.append((cur_parent, cur_lvl))
                    
                    # create new list block using the current item
                    newlistblock = self.create_list_block(current_item["marker"])
                    
                    # our new parent needs to be the child of the previous item
                    previous_item = cur_parent["data"][-1]
                    
                    # add the new list block as a child of the previous item
                    previous_item["data"].append(newlistblock)
                    
                    # make the new list block the parent
                    cur_parent = newlistblock
                    
                    # our new list level is created from the the current item
                    cur_lvl = current_item["level"]
                else:
                    cur_parent["data"].append(current_item)
                    break
        
        ## format our final output using the bank
        FormatList(self.bank)
        
        #for _ in bank:
        return root["data"]



def DetermineListType(marker):
    return "ulist" if marker == "- " else "olist"

def ConvertListIntoItems(source:str=""):
    lineitempattern = re.compile(r'(?P<level>^\s*?)(?P<marker>(?:- )|(?:\d+\. ))(?P<data>(?:.*?(?=^\s*?((- )|(\d+\. ))))|(?:.*?$\n?))', re.MULTILINE | re.DOTALL)
    return lineitempattern.finditer(source)
    
def FormatList(lst):
    for _ in lst:
      if "marker" in _:
        del _["marker"]
      if "level" in _:
        del _["level"]


        
class OListPattern(BasePattern):
    """
    olist
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("olist", OLIST_PATTERN, *args, **kwargs)
        self.item_bank = []


class UListPattern(BasePattern):
    """
    ulist
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("ulist", ULIST_PATTERN, *args, **kwargs)
        