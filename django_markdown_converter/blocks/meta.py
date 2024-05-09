from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import META_BLOCK_DATA
'''
this needs to be expanded more to facilitate
different data types in the meta
for example, it should be able to parse a list of items, links
etc
'''

class MetaBlockifier(BaseBlockifier):
    """ Process meta """
    __slots__ = ("lam_split", "lam_filter", "lam_dict",)

    def __init__(self, *args, **kwargs) -> None:
            super().__init__(**META_BLOCK_DATA)
            
    def setUp(self, *args, **kwargs) -> None:
        self.lam_split = lambda x: x.strip().split(":")
        self.lam_filter = lambda x: len(x)==2
        self.lam_dict = lambda x: (x[0].strip(), x[1].strip())

    def testFor(self, content:str=""):
        '''
        a meta block will have the --- fences
        it will also contain a new line seperated list of
        essentially definitions.

        i need to check this , as it might have bad logic
        we need to test that te before string is empty
        and if its empty , it means its a meta block
        '''
        match = self.pattern.search(content)
        if match:
            before = content[:match.start()]
            before.strip()
            if not before:
                return True
        return False

    def extract_meta(self, content:str=""):
        '''
        a meta block will have the --- fences
        it will also contain a new line seperated list of
        essentially definitions.

        i need to check this , as it might have bad logic
        we need to test that te before string is empty
        and if its empty , it means its a meta block
        '''
        match = self.pattern.search(content)
        if match and match.group("content"):
            content = match.group("content")
            return self.process_meta(content.split("\n"))
        return {
            "type": self.name,
            "tag": self.tag,
            "data": {}
        }

    def process_meta(self, lines):
        return dict(map(self.lam_dict, filter(self.lam_filter, map(self.lam_split, lines))))

    def getProps(self, *args, **kwargs):
        return {}

    def getData(self, lines, *args, **kwargs):
        return self.process_meta(lines)
