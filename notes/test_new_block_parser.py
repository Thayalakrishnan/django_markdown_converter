#%%
import re
from typing import Union, List

path_to_file = "notes/examples/post.md"

MD = """---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---

## Pargraphs

Pargraph 4 **eos** aperiam dolorem numquam quisquam [^1]. Cupiditate ==reprehenderit== beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus `code` voluptates _similique_. Aut maiores hic laudantium distinctio[^2]. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit^5^ ex aspernatur eius ~~consectetur~~ blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.

To include a link, we place the link text in brackets and immediately follow it with the link text in parentheses like [this link](https://lawen.thayalakrishnan.com) to the homepage! We can emphasise **[the link](https://lawen.thayalakrishnan.com)** by enclosing the markdown in double asterisks. The same applies to single asterisk to italise [the link](https://lawen.thayalakrishnan.com). Use angle brackets, to render the link raw <https://lawen.thayalakrishnan.com>. This is an email address <example@email.com> in the middle of a paragraph!

## Image

![ This is an example of a basic image in markdown with a caption ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image2.jpg "Title for a basic image with a caption")

"""

ALL_CONTENT = ".+?"

CASES = [
    ## symettrical
    [(r"```", ALL_CONTENT, r"```"), "code"],
    [(r"---", ALL_CONTENT, r"---"), "meta"],
    [(r"- ", ALL_CONTENT, r""), "ulist"],
    [(r"1. ", ALL_CONTENT, r""), "olist"],
    [(r"\[\^", ALL_CONTENT, r""), "footnote"],
    [(r"!!!", ALL_CONTENT, r""), "admonition"],
    [(r"", r"---", r""), "hr"],
    [(r"", r": .+?", r""), "dlist"],
    [(r"\| ", ALL_CONTENT, r""), "table"],
    [(r"#{1,6} ", ALL_CONTENT, r""), "heading"],
    [(r"\!\[", ALL_CONTENT, r""), "image"],
    [(r"\> ", ALL_CONTENT, r""), "blockquote"],
    [(r"<svg", ALL_CONTENT, r"</svg>"), "svg"],
    [(r"", r"^$", r""), "empty"],
    [(r"", r"[^\n]+?", r""), "paragraph"],
]

lambda_extractor = lambda pat: lambda x: x[len(pat[0]):len(pat[1])*(-1)]
lambda_formatter = lambda pat: lambda x: f"{pat[0]}{x}{pat[1]}"

# pat: pattern <tuple>
single_pattern = lambda label, pat: f"(?P<{label}>{(pat[0])}{(pat[1])}{(pat[2])})" 
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
wrap_pattern = lambda pat: f"(?:{pat})" # label: label <string>, pat: pattern <tuple>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>

# processing content
get_text_captured = lambda cur, content: content[cur[0]:cur[1]]
get_text_between = lambda pre, cur, content: content[pre[1]:cur[0]]
get_text_after = lambda cur, content: content[cur[1]::]
create_text_object = lambda content: {"type": "text", "data": content}
create_markup_object = lambda name, content, lookup: {"type": name, "data": lookup[name](content)}

#EXTRACT = {}
#FORMAT = {}

class Pattern:
    
    def __init__(self, pattern_object:list=[]) -> None:
        """
        patterns is a list of patterns that correspond to the same
        markup. so we chose the first pattern from the list to represent
        the patterns
        """
        label = pattern_object[1]
        pat = pattern_object[0]
        left, middle, right = pat
        
        ## functions
        self.extract = lambda x: x[len(left):len(right)*(-1)]
        self.format = lambda x: f"{left}{x}{right}"
        
        ## regex patterns
        self.re_pattern = single_pattern(label, pat)
        self.label = label
        

class PatternManager:
    
    def __init__(self, cases:list=[]) -> None:
        self.EXTRACT = {}
        self.FORMAT = {}
        self.PATTERNS = []
        self.RE_INLINE_PATTERNS = self.generate_regex(cases)
        
    def create_pattern(self, case):
        return Pattern(case)
    
    def add_pattern(self, case):
        pat = self.create_pattern(case)
        self.EXTRACT[pat.label] = pat.extract
        self.FORMAT[pat.label] = pat.format
        self.PATTERNS.append(pat.re_pattern)
        
    def add_patterns(self, cases):
        for case in cases:
            self.add_pattern(case)
        
    def generate_regex(self, cases):
        self.add_patterns(cases)
        #patterns = label_pattern("block", join_patterns(self.PATTERNS)) 
        patterns = wrap_pattern(join_patterns(self.PATTERNS)) 
        patterns = f"^{patterns}" + r"(?:\n^\{(?P<props>.*?)\})?" + r"(?=\n^\n)"
        print(patterns)
        return re.compile(patterns, re.MULTILINE | re.DOTALL)
    
    
    def find_and_convert_inline(self, source:str="", bank:list=[]) -> Union[str, List]:
        """
        using our inline markup pattern, create a generator
        that will return non overlapping markup
        use this to split the text.
        return a list of converted blocks or the source string
        """
        pos_previous = (0,0)
        pos_current = (0,0)
        
        positions = [(0,0)]
        non_overlapping_content = []

        matches = self.create_inline_markup_iterator(source)

        for _ in matches:
            pos_previous = positions[-1]
            # last group returns the last group to match
            # which in our case is the only group to match
            name = _.lastgroup

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
            new_captured = self.create_inline_markup_block(name, text_captured)
            non_overlapping_content.append(new_captured)
            bank.append(new_captured)

            # set the previous position to the current position
            positions.append(pos_current)
            #pos_previous = pos_current

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
    
    def loop_over(self, source:str="") -> Union[str, List]:
        """
        using our inline markup pattern, create a generator
        that will return non overlapping markup
        use this to split the text.
        return a list of converted blocks or the source string
        """
        pos_previous = (0,0)
        pos_current = (0,0)
        positions = [(0,0)]
        matches = self.create_inline_markup_iterator(source)
        
        for _ in matches:
            pos_previous = positions[-1]
            name = _.lastgroup
            pos_current = _.span()
            #print(f"{name} | previous pos: {pos_previous} current pos: {pos_current}")
            print(f"{name} ---------------")
            block = _.group(name)
            print(block)
            positions.append(pos_current)
        return source


    def convert_recursively(self, blocklist:list=[], level:int=1, bank:list=[]):
        """
        receive a list of blocks
        loop over the blocks until we are not converting nothing no more
        
        we are making the assumption that any blocks of type 'text' do not have
        any inline markup. the logic being that we are jumping from inline markup 
        chosing the next markup object that is both largest and soonest. 
        """
        for block in blocklist:
            if block["type"] != "text" and isinstance(block["data"], str):
                converted = self.find_and_convert_inline(block["data"], bank)
                if isinstance(converted, list) and len(converted):
                    block["data"] = converted
                    self.convert_recursively(block["data"], level+1, bank)
        return


    def convert(self, source:str="") -> list:
        mybank = []
        block_root = {"type": "root", "data": source}
        block_data_as_list = [block_root]
        self.convert_recursively(block_data_as_list, 1, mybank)

        #for _ in filter(lambda x: isinstance(x["data"], str), mybank):
        #    print(_)
        return block_root["data"]


    def revert(self, blocklist:list=[]) -> str:
        current_level = []
        for b in blocklist:
            if isinstance(b["data"], list):
                b["data"] = self.revert(b["data"])
            if isinstance(b["data"], str):
                if b["type"] != "text":
                    line = self.format_content(b)
                    current_level.append(line)
                else:
                    current_level.append(b["data"])
        return "".join(current_level)
    
    
    def create_inline_markup_iterator(self, source:str=""):
        return self.RE_INLINE_PATTERNS.finditer(source)
    
    def create_inline_markup_block(self, name:str="", content:str=""):
        return {"type": name, "data": self.extract_content(name, content)}

    def extract_content(self, name:str="", content:str=""):
        return self.EXTRACT[name](content)
    
    def format_content(self, block:dict={}):
        return self.FORMAT[block["type"]](block["data"])


pm = PatternManager(CASES)
converted = pm.loop_over(MD)
#print(converted)

#reverted = pm.revert(converted)
#print(reverted)

#if MD == reverted:
#    print("correct")
#else:
#    print(repr(MD))
#    print(repr(reverted))
print("done")

# %%
