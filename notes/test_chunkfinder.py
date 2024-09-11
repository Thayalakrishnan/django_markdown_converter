from django_markdown_converter.helpers.helpers import ReadSourceFromFile, WriteToMDFile, WriteJSONToFile
from django_markdown_converter.helpers.processors import process_input_content, extract_meta_block, process_props, process_meta_block
from django_markdown_converter.helpers.parsers import block_parser
from django_markdown_converter.patterns.procpats import PATTERN_DICT

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""
root = []
json_root = []
json_root_nu = []
path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)

print("processed -------------------------")


raw_chunk = process_input_content(raw_chunk)
raw_chunk, meta = extract_meta_block(raw_chunk)

#print(meta)

for index, label, content, props in block_parser(raw_chunk):
    print(f"{index} -------- {label}")
    root.append(f"{index} -------- {label}")
    root.append(content)
    
    current_block = PATTERN_DICT[label].convert(content, props)
    json_root_nu.append(current_block)
    
    json_root.append({
        "blocktype": label,
        "props": process_props(props),
        "data": content
    })
    


#print(json_root)

#write_to_file = "notes/examples/post_output"
write_to_json_file = "notes/examples/post_output.json"
write_to_json_file_nu = "notes/examples/post_output_nu.json"

"""
md = "\n".join(root)
"""

#WriteToMDFile(write_to_file, md)
#yeet = process_props(' id="small-table" caption="small table of values" ')
#WriteJSONToFile(write_to_json_file, json_root)
WriteJSONToFile(write_to_json_file_nu, json_root_nu)