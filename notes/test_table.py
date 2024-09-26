# %%
import re

single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})" # pat: pattern <tuple>
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>

class Pattern:
    
    def __init__(self, name:str="", pats:list=[]) -> None:
        """
        patterns is a list of patterns that correspond to the same
        markup. so we chose the first pattern from the list to represent
        the patterns
        """
        self.name = name
        left, right = pats[0]
        
        ## functions
        self.extract = lambda x: x[len(left):len(right)*(-1)]
        self.format = lambda x: f"{left}{x}{right}"
        
        ## regex patterns
        self.re_pattern = generate_pattern(name, pats)
        

class PatternManager:
    
    def __init__(self, cases:list=[]) -> None:
        self.EXTRACT = {}
        self.FORMAT = {}
        self.PATTERNS = []
        self.RE_INLINE_PATTERNS = self.generate_regex(cases)
        
    def create_pattern(self, name, pat):
        return Pattern(name, pat)
    
    def add_pattern(self, name, pats):
        pat = self.create_pattern(name, pats)
        self.EXTRACT[name] = pat.extract
        self.FORMAT[name] = pat.format
        self.PATTERNS.append(pat.re_pattern)
        
    def add_patterns(self, cases):
        for case in cases:
            pats, name = case
            self.add_pattern(name, pats)
        
    def generate_regex(self, cases):
        self.add_patterns(cases)
        return re.compile(join_patterns(self.PATTERNS))

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
]


pm = PatternManager(CASES)

INLINE_MARKUP_PATTERN  = pm.RE_INLINE_PATTERNS
EXTRACT = pm.EXTRACT
FORMAT = pm.FORMAT

print(INLINE_MARKUP_PATTERN)
print(EXTRACT)
print(FORMAT)
# %%
