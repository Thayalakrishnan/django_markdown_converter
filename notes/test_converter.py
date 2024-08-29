# %%
from django_markdown_converter.blockify import Blockify
from django_markdown_converter.helpers.helpers import ReadSourceFromFile


from pathlib import Path
import os

    
md = """
# Heading 1

Voluptatem eos aperiam dolorem numquam quisquam. 
Cupiditate reprehenderit beatae ab inventore libero. 
Accusantium explicabo optio debitis magni sint earum excepturi. 
Dicta aliquid cupiditate. 
Consequuntur temporibus maxime voluptates similique. 
Aut maiores `Inline code` hic laudantium distinctio. 
Aliquid magni expedita voluptatem illo laudantium illo. 
Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis. 
Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. 
Fuga iste in.

"""

#output = Blockify(md)
#print(output)


current_working_directory = os.getcwd()
root_path = os.path.abspath(os.sep)
#print("current_working_directory:", current_working_directory)
#print("Current root path:", root_path)

#path_to_file = "tests/examples/post.md"
#md = ReadSourceFromFile(path_to_file)
#print(md)

output = Blockify(md)
print(output)
#output = []
#assert isinstance(output, dict)

# %%
