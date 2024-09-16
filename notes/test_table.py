# %%
import re

header = "| Column 1 Title | Column 2 Title |\n"
body = "| Row 1 Column 1| Row 1 Column 2 |\n| Row 2 Column 1| Row 2 Column 2 |\n"
            
            
def get_row(line:str="") -> list:
    """strip leading and trailing pipes,"""
    line = line.strip("|\n ")
    return [_.strip() for _ in line.split("|")]
    
def get_rows(chunk:str="")-> list:
    lines = chunk.split("\n")
    return [get_row(line) for line in lines if len(line)]



print(get_row(header))
print(get_rows(body))
# %%
