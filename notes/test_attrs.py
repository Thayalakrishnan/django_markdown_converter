# %%
import re

md = """## Pargraphs { blocktype="heading" }

Pargraph 1.
{ blocktype="paragraph" }

Pargraph 2. 
{ blocktype="paragraph" }

## Image

![ alt text ](https://amazonaws.com/media/image2.jpg "Image Title")
{ blocktype="image" caption="image caption." }

"""

# generic block level element
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```.*?\n^\n|.*?\n\n)'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))(?:\s*?\{(?P<props>.*?)\}\s*?)?^\n'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))(?:\s*?\{(?P<props>.[^\}]*?)\}\s*?)?^\n'
BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)

#return excise(content=content, target=r'\{(?P<props>.*?)\}', after="(?P<after>$)")


matches = BLOCK_PATTERN.finditer(md)
for m in matches:
    #print(m)
    print(m.groupdict())
# %%
