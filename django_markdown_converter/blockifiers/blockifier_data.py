#from django_markdown_converter.blocks.admonition import AdmonitionBlockifier
#from django_markdown_converter.blocks.blockquote import BlockquoteBlockifier
#from django_markdown_converter.blocks.code import CodeBlockifier
#from django_markdown_converter.blocks.heading import HeadingBlockifier
#from django_markdown_converter.blocks.hr import HRBlockifier
#from django_markdown_converter.blocks.image import ImageBlockifier
#from django_markdown_converter.blocks.meta import MetaBlockifier
#from django_markdown_converter.blocks.footnote import FootnoteBlockifier
#from django_markdown_converter.blocks.table import TableBlockifier
#from django_markdown_converter.blocks.paragraph import ParagraphBlockifier
#from django_markdown_converter.blocks.list import ListBlockifier
#from django_markdown_converter.blocks.definitionlist import DefinitionListBlockifier
#from django_markdown_converter.blocks.svg import SVGBlockifier
#from django_markdown_converter.blocks.empty import EmptyBlockifier

TAB_LENGTH = 4

META_BLOCK_DATA = {
    "pattern": r'^---\s*\n(?P<content>.*?)\n\s*---\s*(?:\n\s*|$)',
    "name": "meta",
    "priority": 10,
    "left": "---",
    "right": "---",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": MetaBlockifier,
}
LIST_BLOCK_DATA = {
    "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
    "name": "list",
    "priority": 20,
    "left": "- ",
    "right": "",
    "singleline": False,
    "nested": True,
    "nestedpriority": 5,
    #"class": ListBlockifier,
}
LIST_BLOCK_DATA = {
    "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
    "name": "ordered",
    "priority": 30,
    "left": "1.",
    "right": "",
    "singleline": False,
    "nested": True,
    "nestedpriority": 4,
    #"class": ListBlockifier,
}
DEFINITIONLIST_BLOCK_DATA = {
    "pattern": r'^\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$)',
    "name": "definitions",
    "priority": 40,
    "left": ": ",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": DefinitionListBlockifier,
}
FOOTNOTE_BLOCK_DATA = {
    "pattern": r'\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
    "name": "footnotes",
    "priority": 50,
    "left": "[^",
    "right": "",
    "singleline": False,
    "nested": True,
    "nestedpriority": 3,
    #"class": FootnoteBlockifier,
}
ADMONITION_BLOCK_DATA = {
    "pattern": r'!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
    "name": "admonition",
    "priority": 60,
    "left": "!!! ",
    "right": "",
    "singleline": False,
    "nested": True,
    "nestedpriority": 2,
    #"class": AdmonitionBlockifier,
}
CODE_BLOCK_DATA = {
    "pattern": r'(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<content>.*?)(?<=\n)(?P<stop>(?:```))\s*',
    "name": "code",
    "priority": 70,
    "left": "```",
    "right": '```',
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": CodeBlockifier,
}
TABLE_BLOCK_DATA = {
    "pattern": r'(?:^\|\s*\{(?P<attrs>.*?)\}\s*\|\s*\n)(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n|\|$))+)',
    "name": "table",
    "priority": 80,
    "left": "|",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": TableBlockifier,
}
BLOCKQUOTE_BLOCK_DATA = {
    "pattern": r'(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<content>(?:\>\s+.*(?:\n|$))+)',
    "name": "blockquote",
    "priority": 90,
    "left": "> ",
    "right": "",
    "singleline": False,
    "nested": True,
    "nestedpriority": 1,
    #"class": BlockquoteBlockifier,
}
HR_BLOCK_DATA = {
    "pattern": r'\n\*\*\*\n',
    "name": "hr",
    "priority": 100,
    "left": "***",
    "right": "",
    "singleline": True,
    "nested": False,
    "nestedpriority": 0,
    #"class": HRBlockifier,
}
HEADING_BLOCK_DATA = {
    "pattern": r'^(?P<level>#{1,6})\s*(?P<content>.*?)(?:\{(?P<attrs>.*?)\})?\s*(?:\n|$)',
    "name": "heading",
    "priority": 110,
    "left": "#",
    "right": "",
    "singleline": True,
    "nested": False,
    "nestedpriority": 0,
    #"class": HeadingBlockifier,
}
IMAGE_BLOCK_DATA = {
    "pattern": r'!\[(?P<attrs>.*?)\]\((?P<content>.*?)\)',
    "name": "image",
    "priority": 120,
    "left": "![",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": ImageBlockifier,
}
SVG_BLOCK_DATA = {
    "pattern": r'\<svg(?P<attrs>.*?)\>(?P<content>.*?)\<\/svg\>',
    "name": "svg",
    "priority": 130,
    "left": "<svg",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": SVGBlockifier,
}
PARAGRAPH_BLOCK_DATA = {
    "pattern": r'(?P<content>(?:.*(?:\n|$))+)',
    "name": "paragraph",
    "priority": 140,
    "left": "",
    "right": "",
    "singleline": False,
    "nested": False,
    "nestedpriority": 0,
    #"class": ParagraphBlockifier,
}


#BLOCKIFIER_DATA = [
#    META_BLOCK_DATA,
#    LIST_BLOCK_DATA,
#    LIST_BLOCK_DATA,
#    DEFINITIONLIST_BLOCK_DATA,
#    FOOTNOTE_BLOCK_DATA,
#    ADMONITION_BLOCK_DATA,
#    CODE_BLOCK_DATA,
#    TABLE_BLOCK_DATA,
#    BLOCKQUOTE_BLOCK_DATA,
#    HR_BLOCK_DATA,
#    HEADING_BLOCK_DATA,
#    IMAGE_BLOCK_DATA,
#    SVG_BLOCK_DATA,
#    PARAGRAPH_BLOCK_DATA,
#]