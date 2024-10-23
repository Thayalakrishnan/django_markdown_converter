import time, gc

from notes.class_tokenizer import run_tokenizer
from notes.class_megatokenizer import run_mega_tokenizer
from notes.class_ogtokenizer import run_ogtokenizer, run_new_ogtokenizer
from notes.testing_newdata import run_new_mega_tokenizer_with_attrs

from notes.tools import get_source

"""
from testing the three ways to tokenize, it seems like using finditer 
along with creating a pattern that incorporates all the block patterns
is the quickest way to do things:
- tokenizer: uses inbuild re.Scanner class
- og: uses our old algorithm of using match.finditer to search for blocks and then using a loop to match blocks individually till we find the right one
- mega: creates a pattern combining all the block patterns. then uses match.finditer to scan the source content. 
- new mega with attrs: creates a pattern combining all the block patterns as well as attrs/props

measured average run time for 10*1000 runs:
- run_ogtokenizer: 0.659 ms
- run_tokenizer: 1.362 ms
- run_mega_tokenizer: 0.355 ms
"""
PATH_TO_FILE = "notes/examples/post.md"

def runtokenizer(tokenizer_func, source):
    tokenizer = tokenizer_func(source)
    for new in tokenizer:
        pass
    return

def loop_run_tokenizer(tokenizer_func, source, runs):
    start_time = time.perf_counter()
    for i in range(runs):
        runtokenizer(tokenizer_func, source)
    end_time = time.perf_counter()
    net_time = (end_time - start_time)/runs
    return net_time


def loop_loop_tokenizer():
    source = get_source(PATH_TO_FILE)
    
    inner_loops = 100
    outer_loops = 100
    
    funcies = [
        run_new_ogtokenizer,
        run_ogtokenizer,
        run_tokenizer,
        run_mega_tokenizer,
        run_new_mega_tokenizer_with_attrs,
    ]
    
    loop_times = [0 for _ in funcies]
    
    for _ in range(outer_loops):
        for index, funky in enumerate(funcies):
            loop_times[index] += loop_run_tokenizer(funky, source, inner_loops)
            gc.collect()
        gc.collect()
        
    for index, funky in enumerate(funcies):
        print(f"'{funky.__name__}' average total {(loop_times[index]/outer_loops) * 1000:.3f} ms")


loop_loop_tokenizer()

#@timer
def compare_tokenizer():
    
    source = get_source(PATH_TO_FILE)
    
    mtk = run_mega_tokenizer(source)
    ogtk = run_ogtokenizer(source)
    tk = run_tokenizer(source)
    
    for m,og,tk in zip(mtk, ogtk, tk):
        if m != og or m != tk or og != tk:
            print(f"mega: {m} | old: {og} | new: {tk}")        
    return

#compare_tokenizer()
    
print(f"done")