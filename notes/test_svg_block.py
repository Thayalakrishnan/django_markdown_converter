import re


raw_chunk = """<svg content></svg>

Sentence to start the paragraph.
Another Sentence part of the first paragraph!

New sentence for new paragraph.
This sentence is for the new paragraph.

"""

chunk = "\n".join(raw_chunk)
chunk = raw_chunk
raw_pattern = r'^(?P<content>.*?)(?:\n\n)(?P<after>.*?)$'
#pattern = re.compile(raw_pattern, re.MULTILINE | re.DOTALL)
pattern = re.compile(raw_pattern, re.DOTALL)

match = pattern.search(chunk)

if match:
    #print(match.groups())
    print(match.groupdict())
