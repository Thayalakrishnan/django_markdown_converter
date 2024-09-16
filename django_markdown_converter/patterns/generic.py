import re

# generic block level element
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```|.*?)\n^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)^\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```\n|.*?\n)\n'
BLOCK_PATTERN_RAW = r'(?P<block>```.*?```.*?\n^\n|.*?\n\n)'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))^\n'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))(?:\s*?\{(?P<props>.*?)\}\s*?)?^\n'
BLOCK_PATTERN_RAW = r'(?P<block>(```.*?```.*?)|(.*?))(?:\s*?\{(?P<props>.[^\}]*?)\}\s*?)?^\n' ## works
BLOCK_PATTERN_RAW = r'(?P<block>^(?:```.*?```.*?)|(?:.*?))(?:^\{(?P<props>.*?)\} *?$\n)?^\n' ## works

"""
(?:(?:^```.*?```.*?)|(?:^.*?))(?P<props>\s*?\{(?:.[^\}]*?)\}\s*?)?(?=^\n)
"""
BLOCK_PATTERN = re.compile(BLOCK_PATTERN_RAW, re.MULTILINE | re.DOTALL)
