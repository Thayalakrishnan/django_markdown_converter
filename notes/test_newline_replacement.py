import re
from django_markdown_converter.helpers.helpers import ReadSourceFromFile

EXTRACT_ATTRS = r'(?P<before>.*)\{(?P<attrs>.*?)\}(?P<after>.*)'
NEWLINE_REPLACE = r'\n{3,}'
NEWLINE_REPLACE = r'^\n{2,}'

NEWLINE_REPLACE_RAW = r'^\n{2,}'
NEWLINE_REPLACE_PATTERN = re.compile(NEWLINE_REPLACE_RAW, re.MULTILINE | re.DOTALL)

path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)

raw_chunk = """## heading



This is come content.

This is some other content. 

## This is anothe heading

This is the third sentence. 


"""
print("before -----------------------------")
raw_chunk = raw_chunk.split("\n")
for i in raw_chunk:
    print(repr(i))
raw_chunk = "\n".join(raw_chunk)
raw_chunk = re.sub(NEWLINE_REPLACE_PATTERN, "\n", raw_chunk)
raw_chunk = raw_chunk.split("\n")

print("after ------------------------------")
for i in raw_chunk:
    print(repr(i))

print("done -------------------------------")
