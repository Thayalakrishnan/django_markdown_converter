import re
from django_markdown_converter.helpers.helpers import ReadSourceFromFile


path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)
raw_chunk = raw_chunk.replace("\n\n\n", "\n\n")
#print(repr(raw_chunk))

chunk = raw_chunk
raw_pattern = r'^(?P<chunk>.*?)(\n\n|\n|$)'
raw_pattern = r'^(?P<chunk>.*?)\n\n'
pattern = re.compile(raw_pattern, re.MULTILINE | re.DOTALL)
match = pattern.finditer(chunk)

for index, m in enumerate(match):
    #print(index)
    print(m)