import re
from django_markdown_converter.helpers.helpers import ReadSourceFromFile

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content

BLOCKQUOTE_BLOCK_DATA: ^(?P<content>(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<between>(?:\>\s+.*(?:\n|$))+))
BLOCKQUOTE_BLOCK_DATA: (?:^>\s+.*?$){1,}(?:\n\n|\n$)
"""

META_BLOCK_DATA = r'^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)'
DEFINITIONLIST_BLOCK_DATA = r'(?P<content>\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$))'
FOOTNOTE_BLOCK_DATA = r'(?P<content>\[\^(?P<index>.+?)\]:\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'
ADMONITION_BLOCK_DATA = r'(?P<content>!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<between>(?: {4,}.*(?:\n|$))+))'
CODE_BLOCK_DATA = r'(?P<content>(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<between>.*?)(?<=\n)(?P<stop>(?:```))\s*)'

HR_BLOCK_DATA = r'^(?P<content>[\*\-]{3,})\s*(?:\n|$)'
TABLE_BLOCK_DATA = r'^(?P<content>(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<between>(?:.*(?:\|\n|\|$))+)(?:(?:\{\s*(?P<attrs>.*?)\s*\})?))'
TABLE_BLOCK_DATA = r'(?P<content>(?:^\|.*?\|\n){1,}(?:\{.*?\})?)'
BLOCKQUOTE_BLOCK_DATA = r'(?P<content>(?:^>\s+.*?$){1,}(?:\n\n|\n$))'

BLOCKQUOTE_BLOCK_DATA = r'(?P<content>(?:\>.*)(?:\n\>.*){1,})(?:\{(?P<attrs>.*?)\})?'
HEADING_BLOCK_DATA = r'^(?P<content>(?P<level>\#{1,6})\s+(?P<text>.*?)(?:\{(?P<attrs>.*?)\})?\s*)(?:\n|$)'
IMAGE_BLOCK_DATA = r'(?P<content>!\[(?P<attrs>.*?)\]\((?P<src>.*?)\))'
SVG_BLOCK_DATA = r'(?P<content><svg\s(?P<attrs>[^>]*)>(?P<between>.*?)</svg>)'
ORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*-\s.*?\n){1,})'
PARAGRAPH_BLOCK_DATA = r'(?P<content>.*?)(?:\n|\n\n|$)'

EXTRACT_ATTRS = r'(?P<before>.*)\{(?P<attrs>.*?)\}(?P<after>.*)'
NEWLINE_REPLACE = r'\n{3,}'
NEWLINE_REPLACE = r'^\n{3,}'
NEWLINE_REPLACE = r'^\n{2,}'
NEWLINE_REPLACE = re.compile(r'^\n{2,}', re.MULTILINE | re.DOTALL)

patterns = [
    ["meta", META_BLOCK_DATA, ["between"]],
    ["definition list", DEFINITIONLIST_BLOCK_DATA, []],
    ["footnote", FOOTNOTE_BLOCK_DATA, []],
    ["admonition", ADMONITION_BLOCK_DATA, []],
    ["code", CODE_BLOCK_DATA, []],
    ["table", TABLE_BLOCK_DATA, []],
    ["blockquote", BLOCKQUOTE_BLOCK_DATA, []],
    ["hr", HR_BLOCK_DATA, []],
    ["heading", HEADING_BLOCK_DATA, []],
    ["image", IMAGE_BLOCK_DATA, []],
    ["svg", SVG_BLOCK_DATA, []],
    ["unordered list", UNORDERED_LIST_BLOCK_DATA, []],
    ["ordered list", ORDERED_LIST_BLOCK_DATA, []],
    ["paragraph", PARAGRAPH_BLOCK_DATA, []],
]



# compile patterns
for p in patterns:
    p[1] = re.compile(p[1], re.MULTILINE | re.DOTALL)


path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)
#raw_chunk = raw_chunk.replace("\n\n\n", "\n\n")
raw_chunk = re.sub(NEWLINE_REPLACE, "\n", raw_chunk)

raw_pattern = r'(?P<chunk>```.*?```|.*?)\n\n'
pattern = re.compile(raw_pattern, re.MULTILINE | re.DOTALL)
match = pattern.finditer(raw_chunk)

pattern_attrs = re.compile(EXTRACT_ATTRS, re.MULTILINE | re.DOTALL)

"""
loop over the content and spit out chunks
"""
for index, m in enumerate(match):
    chunk = m.group("chunk")
    #print("chunk -------------------------")
    print(f"\nchunk {index} --------------------")
    print(repr(chunk))
    # determine the type of block each chunk is
    for label, pattern, items in patterns:
        submatch = pattern.match(chunk)
        if submatch:
            print(f"{label}")
            #print(f"\n{index} - {label} --------------------")
            #content = submatch.group("content")
            
            # check the content for attributes
            #m_attrs = pattern_attrs.match(content)
            #if m_attrs:
            #    # if there are attrs, extract them
            #    print("attrs -------------------------")
            #    print(m_attrs.group("attrs"))
            #    # return the content without the attrs
            #    content = m_attrs.group("before") + m_attrs.group("after")
            #else:
                #print("content -------------------------")
            
            #print(content)
            break

