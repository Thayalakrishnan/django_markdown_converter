# table blockifier
from django_markdown_converter.blocks.base import BaseBlockifier
from django_markdown_converter.blockifiers.blockifier_data import TABLE_BLOCK_DATA


'''
blockifier_table
{
    'type': 'table', 
    'tag': 'table', 
    'data': {
        'header': [
            'Header 1', 
            'Header 2'
        ], 
        'body': [
            ['Row 1, Cell 1', 'Row 1, Cell 2'], 
            ['Row 2, Cell 1', 'Row 2, Cell 2']
        ]
    }
}
'''

class TableBlockifier(BaseBlockifier):
    """ Process tables """
    def __init__(self, *args, **kwargs) -> None:
            super().__init__(**TABLE_BLOCK_DATA)
        
    def getHeader(self, line:str="") -> list:
        """strip leading and trailing pipes,"""
        return [_.strip() for _ in line[1:-1].strip().split("|")]
        
    def getBody(self, lines:list=[])-> list:
        return [[_.strip() for _ in line[1:-1].strip().split("|")] for line in lines]
    
    def get_data(self, lines, *args, **kwargs):
        return {
            "header": self.getHeader(lines[1]),
            "body": self.getBody(lines[3:])
        }