# %%
import re


class Pattern:
    
    def __init__(self, name:str="") -> None:
        self.left = name
        self.right = name

class InlinePattern:
    
    def __init__(self, name:str="") -> None:
        self.pattern = name
        self.patterns = name
        self.count = 0


def lambda_extractor(pat:tuple=()):
    left, right = len(pat[0]), len(pat[1])*(-1)
    return lambda x: x[left:right]

def lambda_formatter(pat:tuple=()):
    left, right = pat
    return lambda x: f"{left}{x}{right}"

CASES = [
    ## symettrical
    [("`", "`"), "code", True],
    [[("**", "**"), ("__", "__")], "strong", True],
    [[("*", "*"), ("_", "_")], "em", True],
    [[("~~", "~~"), ("--", "--")], "del", True],
    [("==", "=="), "mark", True],
    [("``", "``"), "samp", True],
    [(":", ":"), "emoji", True],
    [("^", "^"), "sup", True],
    [("~", "~"), "sub", True],
    [("$", "$"), "math", True],
    
    ## non symettrical
    [("<navlink ", "</navlink>"), "navlink", False],
    [("<", ">"), "rawlink", True],
    [("[^", "]"), "footnote", False],
    [("[", ")"), "link", False],
    #[(" ", " "), "text", True],
]


# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})"

# pats: patterns <list>
or_join_patterns = lambda pats: "|".join(pats)

# label: label <string>, pat: pattern <tuple>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})"

# label: label <string>, pats: patterns <list>
#multi_pattern = lambda pats, label: label_pattern(label, or_join_patterns([single_pattern(pat) for pat in pats]))
multi_pattern = lambda pats, label: label_pattern(label, or_join_patterns(map(single_pattern, pats)))

# label: label <string>, pat: pattern <tuple>
simple_pattern = lambda pat, label: label_pattern(label, single_pattern(pat))


def create_inline_markup_patterns(case_list:list=[]):
    generated_pattern_list = []
    extract_dict = {}
    format_dict = {}
    
    for case in case_list:
        patterns, key, issymettrical = case
        
        if isinstance(patterns, list):
            # multipattern: get the first pattern
            pat = patterns[0]
            cpattern = multi_pattern(pat, key)
        else:
            pat = patterns
            cpattern = simple_pattern(pat, key)

        extract_dict[key] = lambda_extractor(pat)
        format_dict[key] = lambda_formatter(pat)
        
        generated_pattern_list.append(cpattern)
        
    joined_pattern_list = or_join_patterns(generated_pattern_list)
    compiled_pattern_list = re.compile(joined_pattern_list)
    
    return compiled_pattern_list, extract_dict, format_dict


INLINE_MARKUP_PATTERN, EXTRACT, FORMAT = create_inline_markup_patterns(CASES)

print(INLINE_MARKUP_PATTERN)
print(EXTRACT)
print(FORMAT)
# %%
