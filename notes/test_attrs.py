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

block = {
    "type": "svg",
    "props": {
        "title": "generic title"
    },
    "type": "content"
}


generate_attrs = lambda k: f'{k[0]}="{k[1]}"'
pad_if_present = lambda x: f' {x}' if len(x) else f''
wrap_html_content = lambda t, a, c: f'<{t}{pad_if_present(a)}>{c}</{t}>'

props = block.get("props", {})
print(props)
print(list(props.items()))

props = [('title', 'generic title')]

print(list(map(generate_attrs, props)))
attrs = ""

#if props:
#    attrs = " ".join(list(map(generate_attrs, props)))
# %%
