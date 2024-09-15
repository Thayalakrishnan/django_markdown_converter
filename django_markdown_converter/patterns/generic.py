import re

# generic block level element
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```.*?\n^\n|.*?\n\n)'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))^\n'
BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)
