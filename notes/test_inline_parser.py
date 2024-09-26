#%%
import re
from typing import Union, List

"""
pattern
key
symmetrical
"""
CASES = [
    ## symettrical
    [[("`", "`")], "code"],
    [[("**", "**"), ("__", "__")], "strong"],
    [[("*", "*"), ("_", "_")], "em"],
    [[("~~", "~~"), ("--", "--")], "del"],
    [[("==", "==")], "mark"],
    [[("``", "``")], "samp"],
    [[(":", ":")], "emoji"],
    [[("^", "^")], "sup"],
    [[("~", "~")], "sub"],
    [[("$", "$")], "math"],
    
    ## non symettrical
    [[("<navlink ", "</navlink>")], "navlink"],
    [[("<", ">")], "rawlink"],
    [[("[^", "]")], "footnote"],
    [[("[", ")")], "link"],
    #[(" ", " "), "text", True],
]

lambda_extractor = lambda pat: lambda x: x[len(pat[0]):len(pat[1])*(-1)]
lambda_formatter = lambda pat: lambda x: f"{pat[0]}{x}{pat[1]}"

# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})" 
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda pats, label: label_pattern(label, join_patterns([single_pattern(pat) for pat in pats])) # label: label <string>, pats: patterns <list>

# processing content
get_text_captured = lambda cur, content: content[cur[0]:cur[1]]
get_text_between = lambda pre, cur, content: content[pre[1]:cur[0]]
get_text_after = lambda cur, content: content[cur[1]::]
create_text_object = lambda content: {"type": "text", "data": content}
create_markup_object = lambda name, content, lookup: {"type": name, "data": lookup[name](content)}


def create_inline_markup_patterns(case_list:list=[]):
    generated_pattern_list = []
    extract_dict = {}
    format_dict = {}
    
    for case in case_list:
        patterns, name = case
        
        pattern = patterns[0]
        extract_dict[name] = lambda_extractor(pattern)
        format_dict[name] = lambda_formatter(pattern)
        
        compiled_pattern = generate_pattern(patterns, name)
        generated_pattern_list.append(compiled_pattern)
        
    joined_pattern_list = join_patterns(generated_pattern_list)
    compiled_patterns = re.compile(joined_pattern_list)
    return compiled_patterns, extract_dict, format_dict

#EXTRACT = {}
#FORMAT = {}

INLINE_MARKUP_PATTERN, EXTRACT, FORMAT = create_inline_markup_patterns(CASES)

# no flags
#INLINE_MARKUP_PATTERN_RAW = "|".join(compilespatterns)
#INLINE_MARKUP_PATTERN = re.compile(INLINE_MARKUP_PATTERN_RAW)

def find_and_convert_inline(source:str="", bank:list=[]) -> Union[str, List]:
    """
    using our inline markup pattern, create a generator
    that will return non overlapping markup
    use this to split the text.
    return a list of converted blocks or the source string
    """
    pos_previous = (0,0)
    pos_current = (0,0)
    non_overlapping_content = []

    matches = INLINE_MARKUP_PATTERN.finditer(source)

    for _ in matches:
        # last group returns the last group to match
        # which in our case is the only group to match
        group_key = _.lastgroup

        # get the current position of the match
        pos_current = _.span()

        # extract the text between the previous match and the current match
        text_between = get_text_between(pos_previous, pos_current, source)
        if len(text_between):
            # if its too small, let it go, it aint worth it
            new_between = create_text_object(text_between)
            non_overlapping_content.append(new_between)
            bank.append(new_between)

        # extract the text captured
        text_captured = get_text_captured(pos_current, source)
        new_captured = create_markup_object(group_key, text_captured, EXTRACT)
        non_overlapping_content.append(new_captured)
        bank.append(new_captured)

        # set the previous position to the current position
        pos_previous = pos_current

    if len(non_overlapping_content):
        # make sure we only do this if there is content before
        text_after = get_text_after(pos_current, source)
        if len(text_after):
            # if its too small, let it go, it aint worth it
            new_after = create_text_object(text_after)
            non_overlapping_content.append(new_after)
            bank.append(new_after)

    if len(non_overlapping_content):
        return non_overlapping_content
    return source


def loop_over_data_and_conver_inline(blocklist:list=[], level:int=1, bank:list=[]):
    """
    receive a list of blocks
    loop over the blocks until we are not converting nothing no more
    """
    for block in blocklist:
        if block["type"] != "text" and isinstance(block["data"], str):
            converted = find_and_convert_inline(block["data"], bank)
            if isinstance(converted, list) and len(converted):
                block["data"] = converted
                loop_over_data_and_conver_inline(block["data"], level+1, bank)
    return


def convert(source:str="") -> list:
    mybank = []
    block_root = {"type": "root", "data": source}
    block_data_as_list = [block_root]
    loop_over_data_and_conver_inline(block_data_as_list, 1, mybank)

    #for _ in filter(lambda x: isinstance(x["data"], str), mybank):
    #    print(_)
    return block_root["data"]


def revert(blocklist:list=[]) -> str:
    current_level = []
    for b in blocklist:
        if isinstance(b["data"], list):
            b["data"] = revert(b["data"])
        if isinstance(b["data"], str):
            if b["type"] != "text":
                line = FORMAT[b["type"]](b["data"])
                current_level.append(line)
            else:
                current_level.append(b["data"])
    return "".join(current_level)


MD = [
    """**Markdown Example** with _**Inline Markup**_.""",
    """This is a **bold** statement, and this is an _italicized_ one.""",
    """You can even combine them to make text _**both italic and bold**_.""",
    """If you need to reference a link, here's a [link to Markdown documentation](https://www.markdownguide.org).""",
    """This item has some inline markup like _italics_ and **bold** text.""",
    """Nested list item with a [link to a website](https://example.com) and some `inline code`.""",
    """Even deeper nesting: _Italicized_ **bold** list item with `code` inline.""",
    """Another item with **nested** inline **markup**.""",
    """This list item uses some `inline code` and ends with _**italicized and bold**_ text.""",
    """To write code, you can use backticks for `inline code`, like this.""",
]
MD = " ".join(MD)

converted = convert(MD)
print(converted)
reverted = revert(converted)
print(reverted)

print("done")

# %%
