import re
from typing import Callable, Pattern

#from .inline_data import CASES_LIST
from django_markdown_converter.inlineifiers.inline_data import CASES_LIST

class InlinePatternClass:
    """
    inline patterns case
    """
    __slots__ = ("pattern", "length", "tag", "template")
    
    def __init__(self, pattern:Pattern, length:int, tag:str, template:Callable) -> None:
        self.pattern = pattern
        self.length = length
        self.tag = tag
        self.template = template


def build_element_pattern(left:Pattern, middle:Pattern, right:Pattern):
    return re.compile(re.escape(left) + middle + re.escape(right))

def build_patterns(cases_list:list) -> list:
    """using the cases list, build an array of inline patterns to match against"""
    cases = []
    for boundary_case in cases_list:
        left, middle, right = boundary_case["boundary"]
        tag = boundary_case["tag"]
        template = boundary_case["template"]
        pattern = build_element_pattern(left, middle, right)
        length = len(left) + len(right)
        cases.append(InlinePatternClass( pattern, length, tag, template))
    return cases

CASES = build_patterns(CASES_LIST)

def get_content(match):
    """return the matched strings group"""
    return match.group("content").strip()

def get_content_length(match, boundary):
    """return the length of the content (with out the boundary)"""
    return len(match.group(0)) - boundary.length

def replace_match(match, line, replacement):
    """replace the found string with the new string"""
    return line.replace(match.group(0), replacement)

def build_replacement(match, line, boundary):
    """check the content length, if its valid, we can build our replacement
    using the template"""
    if get_content_length(match, boundary):
        return boundary.template(boundary.tag, *match.groupdict().values())
    return line

def extract_and_replace(match, line, boundary):
    """build replacement string and swap them out"""
    replacement = build_replacement(match, line, boundary)
    return replace_match(match, line, replacement)

def recursive_find(boundary, lines:list=[], index:int=0):
    """recursively loop over the given line until there 
    are no more regex matches for the current pattern"""
    match = boundary.pattern.search(lines[index])
    if match:
        lines[index] = extract_and_replace(match, lines[index], boundary)
        recursive_find(boundary, lines, index)

# testing by lines
def find_by_line(cases:list=[], lines:list=[], index:int=0):
    """for the given line, loop over the boundaries"""
    for boundary in cases:
        recursive_find(boundary, lines, index)

def TestTheLinesCaseByCase(cases:list=[], lines:list=[]):
    """loop over the lines for testing"""
    for index in range(len(lines)):
        find_by_line(cases, lines, index)

# testing by boundary
def find_by_case(boundary, lines:list=[]):
    """loop over the lines for testing"""
    for index in range(len(lines)):
        recursive_find(boundary, lines, index)

def TestTheCasesBoundaryByBoundary(cases:list=[], lines:list=[]):
    """loop over the inline patterns"""
    for boundary in cases:
        find_by_case(boundary, lines)


def InlineParser(lines:list=[]) -> list:
    #TestTheLinesCaseByCase(CASES, lines)
    TestTheCasesBoundaryByBoundary(CASES, lines)
    return lines
    

