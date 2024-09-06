import time, json
from functools import wraps
import re

def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Execution of '{func.__name__}' took {(end_time - start_time) * 1000:.3f} milliseconds")
        return result
    return wrapper_timer


LAMBDA_HELPERS = {
    "strip_source": lambda x: x.strip(),
    "remove_empties": lambda x: len(x),
    "leftstrip": lambda x: x.lstrip(),
    "strip-and-split-by-colon": lambda x: x.strip().split(":"),
    "filter-len-2": lambda y: len(y)==2,

    "map-array-to-tuple": lambda z: (z[0].strip(), z[1].strip()),
    "map-strip-and-split-by": lambda x, y: x.strip().split(y),

    "filter-empties": lambda x: len(x),
    "filter-len-by": lambda x, y: len(x)==y,
}


def build_single_line_fenced_pattern_given_boundaries(left, right):
    return re.compile(re.escape(left) + r'(?P<content>.*?)' + re.escape(right))


def convert_array_of_colon_separated_values_to_dict(lines):
    return lines

def print_lines(content):
    lines = content.split("\n")
    for i in lines:
        print(repr(i))
    return "\n".join(lines)


def ReadSourceFromFile(read_from:str="") -> str:
    """open markdown file return the contents"""
    with open(read_from, 'r', encoding="utf8") as file:
        source = file.read()
    return source

def ReadJSONFromFile(read_from:str="") -> str:
    """open markdown file return the contents"""
    with open(read_from, 'r') as file:
        data = json.load(file)
    return data


def WriteJSONToFile(write_too:str="", data:list=[]) -> str:
    """write JSON data to file"""
    with open(write_too, "w") as json_file:
        json.dump(data, json_file, indent=4)


def WriteToMDFile(write_too:str="", data:str="") -> str:
    """write string data to Markdown"""
    with open(f"{write_too}.md", "w") as file:
        file.write(data)