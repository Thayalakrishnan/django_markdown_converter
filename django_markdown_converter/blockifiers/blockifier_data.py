TAB_LENGTH = 4

META_BLOCK_DATA = {
    "pattern": r'^---\s*\n(?P<content>.*?)\n\s*---\s*(?:\n\s*|$)',
    "name": "meta",
    "left": "---",
    "right": "---",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 10,
    "nestedpriority": 0,
}
UNORDERED_LIST_BLOCK_DATA = {
    "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
    "name": "list",
    "left": "- ",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": True,
    "priority": 20,
    "nestedpriority": 5,
}

ORDERED_LIST_BLOCK_DATA = {
    "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
    "name": "ordered",
    "left": "1.",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": True,
    "priority": 30,
    "nestedpriority": 4,
}
DEFINITIONLIST_BLOCK_DATA = {
    "pattern": r'^\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$)',
    "name": "definitions",
    "left": ": ",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 40,
    "nestedpriority": 0,
}
FOOTNOTE_BLOCK_DATA = {
    "pattern": r'\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
    "name": "footnotes",
    "left": "[^",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": True,
    "priority": 50,
    "nestedpriority": 3,
}
ADMONITION_BLOCK_DATA = {
    "pattern": r'!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
    "name": "admonition",
    "left": "!!! ",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": True,
    "priority": 60,
    "nestedpriority": 2,
}
CODE_BLOCK_DATA = {
    "pattern": r'(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<content>.*?)(?<=\n)(?P<stop>(?:```))\s*',
    "name": "code",
    "left": "```",
    "right": '```',
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 70,
    "nestedpriority": 0,
}
TABLE_BLOCK_DATA = {
    "pattern": r'^(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n|\|$))+)(?:(?:\{\s*(?P<attrs>.*?)\s*\})?)',
    "name": "table",
    "left": "|",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 80,
    "nestedpriority": 0,
}
BLOCKQUOTE_BLOCK_DATA = {
    "pattern": r'(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<content>(?:\>\s+.*(?:\n|$))+)',
    "name": "blockquote",
    "left": "> ",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": True,
    "priority": 90,
    "nestedpriority": 1,
}
HR_BLOCK_DATA = {
    #"pattern": r'\n\*\*\*\n',
    "pattern": r'^\s*(?P<content>\*\*\*)\s*(?:\n|$)',
    "name": "hr",
    "left": "***",
    "right": "",
    "flagged": False,
    "singleline": True,
    "nested": False,
    "priority": 100,
    "nestedpriority": 0,
}
HEADING_BLOCK_DATA = {
    #"pattern": r'^(?P<level>#{1,6})\s*(?P<content>.*?)(?:\{(?P<attrs>.*?)\})?\s*(?:\n|$)',
    "pattern": r'^(?P<level>#{1,6})\s+(?P<content>.*?)(?:\{(?P<attrs>.*?)\})?\s*(?:\n|$)',
    "name": "heading",
    "left": "#",
    "right": "",
    "flagged": False,
    "singleline": True,
    "nested": False,
    "priority": 110,
    "nestedpriority": 0,
}
IMAGE_BLOCK_DATA = {
    "pattern": r'!\[(?P<attrs>.*?)\]\((?P<content>.*?)\)',
    "name": "image",
    "left": "![",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 120,
    "nestedpriority": 0,
}
SVG_BLOCK_DATA = {
    "pattern": r'\<svg(?P<attrs>.*?)\>(?P<content>.*?)\<\/svg\>',
    "name": "svg",
    "left": "<svg",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 130,
    "nestedpriority": 0,
}
PARAGRAPH_BLOCK_DATA = {
    "pattern": r'(?P<content>(?:.*(?:\n|$))+)',
    "name": "paragraph",
    "left": "",
    "right": "",
    "flagged": False,
    "singleline": False,
    "nested": False,
    "priority": 140,
    "nestedpriority": 0,
}