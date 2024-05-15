import re
from django_markdown_converter.blocks.base import BaseBlockifier
from typing import Generator
from django_markdown_converter.blockifiers.blockifier_data import UNORDERED_LIST_BLOCK_DATA, ORDERED_LIST_BLOCK_DATA

'''
list_ul_processor
'''

class ListBlockifier(BaseBlockifier):
    """ Process list blocks. """
    __slots__ = ("pattern_li", "pattern_ul", "pattern_ol", "pattern_ul_or_ol",)
    
    #def __init__(self, *args, **kwargs) -> None:
    #    super().__init__(**LIST_BLOCK_DATA)
            
    def setUp(self, *args, **kwargs) -> None:
        self.pattern_li = re.compile(r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)')
        self.pattern_ul = re.compile(r'^(\s*)(-)\s+(.+?)(?=\n{2}|$)')
        self.pattern_ol = re.compile(r'^(\s*)(\d+\.)\s+(.+?)(?=\n{2}|$)')
        self.pattern_ul_or_ol = re.compile(r'^(\s*)(\d+\.|-\s+)(.+?)(?=\n{2}|$)')

    def test_line_item(self, line):
        return self.pattern_ul.match(line) or self.pattern_ol.match(line)
        #return self.pattern_ul_or_ol.match(line)

    def get_line_type(self, line):
        return "ul" if self.pattern_ul.match(line) else "ol"
    
    def extract_line_info(self, match):
        return (match.group('indentation'), match.group('marker'), match.group('content'))
    
    def get_list_items(self):
        return self.bank
    
       
    def yieldGroupedLines(self, lines) -> Generator[int, None, None]:
        current_line = []
        for line in lines:
            # test if this is the start of a new li
            if self.test_line_item(line):
                # if the current line  is the start of a new line
                # we need to store the old line before we assign the nwe one 
                # to curren tline
                if current_line:
                    yield current_line
                    
                # set the current line to the new line
                current_line = [line]
            else:
                current_line.append(line.lstrip())
            
        yield current_line
       
    def blockify(self, lines):
        result = []
        stack = []
        ptr_curArr = result
        ptr_preArr = result
        curLevel = 0
        preLevel = 0
        grouped_lines = self.yieldGroupedLines(lines)
        
        for lines in grouped_lines:
            match = self.pattern_li.match("\n".join(lines))
            
            if match:
                loop_count = 0
                indentation, marker, content = self.extract_line_info(match)
                
                curLevel = len(indentation)
                liItem = self.create_list_item(self.get_line_type(lines[0]), curLevel, marker, content)
                
                while(True):
                    # failsafe incase we are looping too much
                    if loop_count > 15:
                        curLevel = preLevel
                        
                    # if the current level is equal, add to current list
                    if curLevel == preLevel:
                        ptr_curArr.append(liItem)
                        break
                    
                    # if the current level is bigger than the previous level, we go deeper
                    elif curLevel > preLevel:
                        
                        # push the previous array pointer on to the stack
                        stack.append(ptr_curArr)
                        
                        # point previous array pointer to the current array
                        ptr_preArr = ptr_curArr
                        
                        # assign the curret array ptr to the a new array
                        ptr_curArr = []
                        
                        # add the current list item to the new array 
                        ptr_curArr.append(liItem)
                        
                        # push this new array to the previous array so that it is nested within
                        ptr_preArr.append(ptr_curArr)
                        
                        # update the current level 
                        preLevel = curLevel
                        break
                    else:
                        # point current array to the previous array as we are closing it up
                        ptr_curArr = ptr_preArr
                        
                        # if there ar e arrays on the stack, get the most recent one and 
                        # point the previous array pointer to it
                        #print(f"----------------------- current stack ")       
                        #print(stack)
                        if len(stack):
                            ptr_preArr = stack.pop()
                        
                        # need to go back two as the last aray is the array we just built up
                        last_item = ptr_curArr[-2]
                        
                        # assign the previous items lasts level to the previous level
                        preLevel = last_item["level"]
                        loop_count += 1

        #print(f"----------------------- flat list ----------------------------")                 
        #print(result)
        return self.process_list_items(result)
        
    def construct_list_item(self, content):
        #print("---------------------")
        #print(content)
        li =  {
            'type': "item",
            'tag': "li",
            'data': content
        }
        self.bank.append(li)
        return li
        
    def create_list_object(self, items, emptyList):
        firstItem = items[0]
        return {
            'type': "list",
            'level': firstItem["level"],
            'tag': firstItem["type"],
            'children': emptyList
        }

    def construct_list(self, items, currentList):

        for item in items:
            if isinstance(item, list):
                newList = []
                currentList.append(self.create_list_object(item, newList))
                self.construct_list(item, newList)
            else:
                newItem = self.construct_list_item(item["content"])
                currentList.append(newItem)

    def process_list_items(self, items):
        emptyList = []    
        self.construct_list(items, emptyList)
        return self.create_list_object(items, emptyList)

    def create_list_item(self, lineType:str, level:int, marker:str, content:str) -> dict:
        return {
            "type": lineType,
            "level": level,
            "delimeter": marker,
            "content": content
        }



class OrderedListBlockifier(ListBlockifier):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**ORDERED_LIST_BLOCK_DATA)
        
class UnOrderedListBlockifier(ListBlockifier):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**UNORDERED_LIST_BLOCK_DATA)