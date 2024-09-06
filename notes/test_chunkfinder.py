from django_markdown_converter.helpers.helpers import ReadSourceFromFile, WriteToMDFile, WriteJSONToFile
from django_markdown_converter.helpers.processors import process_input_content, extract_meta_block, process_props, process_meta_block
from django_markdown_converter.helpers.parsers import block_parser

"""
loop over the content and spit out chunks
process the chunks
create a big block tree
parse the inline content
"""
root = []
json_root = []
path_to_file = "notes/examples/post.md"
raw_chunk = ReadSourceFromFile(path_to_file)

print("processed -------------------------")
raw_chunk = process_input_content(raw_chunk)
raw_chunk, meta = extract_meta_block(raw_chunk)

print(meta)



"""
for index, label, content, props in block_parser(raw_chunk):
    root.append(f"{index} -------- {label}")
    root.append(content)
    json_root.append({
        "blocktype": label,
        "props": process_props(props),
        "data": content
    })

write_to_file = "notes/examples/post_output"
write_to_json_file = "notes/examples/post_output.json"
md = "\n".join(root)
"""


#WriteToMDFile(write_to_file, md)
#WriteJSONToFile(write_to_json_file, json_root)
#yeet = process_props(' id="small-table" caption="small table of values" ')
#print(yeet)