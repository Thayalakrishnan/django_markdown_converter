from django_markdown_converter.helpers.helpers import ReadSourceFromFile, WriteToMDFile, WriteJSONToFile
from django_markdown_converter.helpers.processors import process_input_content, extract_meta_block
from django_markdown_converter.helpers.parsers import block_parser

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

for block in block_parser(raw_chunk):
    json_root_nu.append(block)

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