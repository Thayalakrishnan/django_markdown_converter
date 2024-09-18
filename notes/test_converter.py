# %%
import re
from django_markdown_converter.convert import Convert

md = """Multiline Item 1, line 1.\nMultiline Item 1, line 2.\n\nMultiline Item 1, line 3 after double line break\n"""

converted = Convert(md)
for _ in converted:
  print(_)

