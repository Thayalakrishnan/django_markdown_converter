from django_markdown_converter.helpers.utility import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content
from django_markdown_converter.patterns.classes.base import BasePattern, PatternManager


PATH_TO_FILE = "notes/examples/post.md"

#@timer
def get_source(path):
    #print("processed -------------------------")
    chunk = ReadSourceFromFile(path)
    return process_input_content(chunk)

def run_ogtokenizer(source):
    tk = BasePattern()
    m = tk.tokenize(source)
    for _ in m:
        yield(_[0])
        

def run_ogtokenizer_in_console(path):
    source = get_source(path)
    print(f"run_ogtokenizer_in_console: start")
    m = run_ogtokenizer(source)
    for _ in m:
        print(f"{_}")
    print(f"run_ogtokenizer_in_console: done")
    

#run_ogtokenizer_in_console(PATH_TO_FILE)
#print(f"done")    

# new og
def run_new_ogtokenizer(source):
    tk = PatternManager()
    m = tk.tokenize(source)
    for _ in m:
        yield(_[0])
    
def run_new_ogtokenizer_in_console(path):
    source = get_source(path)
    print(f"run_ogtokenizer_in_console: start")
    m = run_new_ogtokenizer(source)
    for _ in m:
        print(f"{_}")
    print(f"run_ogtokenizer_in_console: done")


#run_new_ogtokenizer_in_console(PATH_TO_FILE)
#print(f"done")