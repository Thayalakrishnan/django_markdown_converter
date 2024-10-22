import re
from django_markdown_converter.patterns.newdata import PATTERNS
from notes.tools import get_source

PATH_TO_FILE = "notes/examples/post.md"
source = get_source(PATH_TO_FILE)

regex_named_group = lambda name, pat: f"(?P<{name}>{pat})"
regex_group = lambda pat: f"(?:{pat})"
BUILT_PATTERNS = []

def flag_setter(flags:dict={}):
    f = ""
    if flags["MULTILINE"]:
        f+= "m"
    if flags["DOTALL"]:
        f+= "s"
    return f

for _ in PATTERNS:
    pattern_list = _["pattern"]
    label = _["type"]
    flags = flag_setter(_["flags"])
    
    pattern_parts = []
    
    for p in pattern_list:
        if isinstance(p, str):
            pattern_parts.append(p)
            continue
        else:
            #pattern.append(regex_named_group(p[0], p[1]))
            pattern_parts.append(f"(?:{p[1]})")
    #BUILT_PATTERNS.append((_["type"], "".join(pattern)))
    pattern = "".join(pattern_parts)
    current_pattern = f"(?P<{label}>(?{flags}:{pattern}))"
    
    BUILT_PATTERNS.append(current_pattern)

PROPS_PATTERN = r".*?(?:^\{(?P<props>.*?)\} *?$\n)?"
PROPS_PATTERN = r"(?m:(?P<props>^\{.*?\}\n))?"
#BLOCK_PATTERN = regex_named_group("block", "|".join(BUILT_PATTERNS))
#BLOCK_PATTERN = regex_named_group("block", "|".join(BUILT_PATTERNS))
BLOCK_PATTERN = regex_group("|".join(BUILT_PATTERNS))


#for _ in BUILT_PATTERNS:
#    print(_)

def extract_block_and_attrs(groupdict:dict={}) -> dict:
    return dict([(k, v) for k,v in groupdict.items() if v])
    

BLOCK_PATTERN = re.compile(f"(?:{BLOCK_PATTERN})" + PROPS_PATTERN)
#print(BLOCK_PATTERN_WITH_PROPS)

matches = re.finditer(BLOCK_PATTERN, source)
#matches = re.finditer(PROPS_PATTERN, source)
counter = 0
for index,_ in enumerate(matches):
    g = _.lastgroup
    #if g not in ["paragraph", "newline"]:
    if g not in ["newline"]:
        if g:
            counter+=1
            print(f"{index}| {counter} | {g}")
            #print(_.group(g))
            print(_.groupdict())
        #if g == "paragraph":
        #    print(_.group(g))


print(f"done")