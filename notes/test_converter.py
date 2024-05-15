# %%
#from django_markdown_converter.blockify import Blockify
from django_markdown_converter.blockify import Blockify
from django_markdown_converter.helpers.helpers import ReadSourceFromFile
from pathlib import Path
import os

    
md = """
# Heading 1

This is a paragraph after a heading. 

"""

#output = Blockify(md)
#print(output)


current_working_directory = os.getcwd()
root_path = os.path.abspath(os.sep)
#print("current_working_directory:", current_working_directory)
#print("Current root path:", root_path)

path_to_file = "tests/examples/post.md"
md = ReadSourceFromFile(path_to_file)
#print(md)

output = Blockify(md)
#output = []
#assert isinstance(output, dict)

# %%
