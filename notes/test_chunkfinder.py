from django_markdown_converter.helpers.utility import ReadSourceFromFile, WriteToMDFile, WriteJSONToFile
from django_markdown_converter.patterns.classes.base import BasePattern, process_input_content


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
#raw_chunk, meta = extract_meta_block(raw_chunk)

BasePattern.InitialiseClasses()

#print(BasePattern.BLOCK_LIST)
print(BasePattern.BLOCK_LOOKUP)

for block in BasePattern.block_parser(raw_chunk):
    json_root_nu.append(block)


#while BasePattern.nested_blocks_parser():
#    continue
#BasePattern.nested_blocks_parser()

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

print("done!")