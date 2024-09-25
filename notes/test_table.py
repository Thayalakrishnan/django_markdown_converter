# %%
import re


class Pattern:
    
    def __init__(self, pat:tuple=(), name:str="") -> None:
        left, right = pat
        
        self.name = name
        self.pattern = f"({re.escape(left)}.+?{re.escape(right)})"
        
        ## functions
        self.extract = lambda x: x[len(left):len(right)*(-1)]
        self.format = lambda x: f"{left}{x}{right}"
        
        self.left = left
        self.right = right
        
class MultiPattern:
    
    def __init__(self, pats:list=[], name:str="") -> None:
        left, right = pats[0]
        self.name = name
        self.patterns = [Pattern(p) for p in pats]
        
        ## functions
        self.extract = lambda x: x[len(left):len(right)*(-1)]
        self.format = lambda x: f"{left}{x}{right}"
        
        self.left = left
        self.right = right
        
        


class PatternManager:
    
    def __init__(self, cases:list=[]) -> None:
        self.EXTRACT = {}
        self.FORMAT = {}
        
        generated_pattern_list = []
        
        for case in cases:
            
            patterns, key = case
            
            if isinstance(patterns, list):
                
                # multipattern: get the first pattern
                pat = patterns[0]
                cpattern = multi_pattern(pat, key)
            else:
                pat = patterns
                cpattern = simple_pattern(pat, key)


            self.EXTRACT[key] = lambda_extractor(pat)
            self.FORMAT[key] = lambda_formatter(pat)
            
            generated_pattern_list.append(cpattern)
            
        joined_pattern_list = or_join_patterns(generated_pattern_list)
        
        self.RE_INLINE_PATTERNS = re.compile(joined_pattern_list)



CASES = [
    ## symettrical
    [("`", "`"), "code"],
    [[("**", "**"), ("__", "__")], "strong"],
    [[("*", "*"), ("_", "_")], "em"],
    [[("~~", "~~"), ("--", "--")], "del"],
    [("==", "=="), "mark"],
    [("``", "``"), "samp"],
    [(":", ":"), "emoji"],
    [("^", "^"), "sup"],
    [("~", "~"), "sub"],
    [("$", "$"), "math"],
    
    ## non symettrical
    [("<navlink ", "</navlink>"), "navlink"],
    [("<", ">"), "rawlink"],
    [("[^", "]"), "footnote"],
    [("[", ")"), "link"],
]


# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})"

# pats: patterns <list>
or_join_patterns = lambda pats: "|".join(pats)

# label: label <string>, pat: pattern <tuple>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})"

# label: label <string>, pats: patterns <list>
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
