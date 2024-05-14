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

"""
| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |
{ id="small-table" caption="small table of values" }
"""


"""
need to add table validation
- right now we are not checking if the converted table is even valid
- for example checking the number columns exracted matches up
"""

class TableBlockifier(BaseBlockifier):
    """ Process tables """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**TABLE_BLOCK_DATA)
        
    def getHeader(self, line:str="") -> list:
        """strip leading and trailing pipes,"""
        return [_.strip() for _ in line[1:-1].strip().split("|")]
        
    def getBody(self, chunk:str="")-> list:
        lines = chunk.split("\n")
        return [[_.strip() for _ in line[1:-1].strip().split("|")] for line in lines if len(line)]
    
    def get_data(self, match, *args, **kwargs):
        return {
            "header": self.getHeader(match.group('header')),
            "body": self.getBody(match.group('content'))
        }