from blockifiers.blockifier_admonition import AdmonitionBlockifier
from blockifiers.blockifier_code import CodeBlockifier
from blockifiers.blockifier_heading import HeadingBlockifier
from blockifiers.blockifier_hr import HRBlockifier
from blockifiers.blockifier_image import ImageBlockifier
from blockifiers.blockifier_meta import MetaBlockifier
from blockifiers.blockifier_footnote import FootnoteBlockifier
from blockifiers.blockifier_blockquote import BlockquoteBlockifier
from blockifiers.blockifier_table import TableBlockifier
from blockifiers.blockifier_paragraph import ParagraphBlockifier
from blockifiers.blockifier_list import ListBlockifier
from blockifiers.blockifier_definitionlist import DefinitionListBlockifier
from blockifiers.blockifier_svg import SVGBlockifier
from blockifiers.blockifier_empty import EmptyBlockifier


TAB_LENGTH = 4

BLOCKIFIER_DATA = [
    {
        "pattern": r'^---\s*\n(?P<content>.*?)\n\s*---\s*(?:\n\s*|$)',
        "name": "meta",
        "priority": 10,
        "left": "---",
        "right": "---",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": MetaBlockifier,
    },
    {
        "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
        "name": "list",
        "priority": 20,
        "left": "- ",
        "right": "",
        "singleline": False,
        "nested": True,
        "nestedpriority": 5,
        "class": ListBlockifier,
    },
    {
        "pattern": r'^(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<content>(?P<item>.+?)(?=\n{1}|$)(?P<rest>(?:\s{0,}.*(?:\n|$))+)?)',
        "name": "ordered",
        "priority": 30,
        "left": "1.",
        "right": "",
        "singleline": False,
        "nested": True,
        "nestedpriority": 4,
        "class": ListBlockifier,
    },
    {
        "pattern": r'^\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$)',
        "name": "definitions",
        "priority": 40,
        "left": ": ",
        "right": "",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": DefinitionListBlockifier,
    },
    {
        "pattern": r'\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
        "name": "footnotes",
        "priority": 50,
        "left": "[^",
        "right": "",
        "singleline": False,
        "nested": True,
        "nestedpriority": 3,
        "class": FootnoteBlockifier,
    },
    {
        "pattern": r'!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)',
        "name": "admonition",
        "priority": 60,
        "left": "!!! ",
        "right": "",
        "singleline": False,
        "nested": True,
        "nestedpriority": 2,
        "class": AdmonitionBlockifier,
    },
    {
        "pattern": r'(?P<start>^(?:```))\s*(\{(?P<attrs>.*?)\})\n(?P<content>.*?)(?<=\n)(?P<stop>(?:```))\s*',
        "name": "code",
        "priority": 70,
        "left": "```",
        "right": '```',
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": CodeBlockifier,
    },
    {
        "pattern": r'(?:^\|\s*\{(?P<attrs>.*?)\}\s*\|\s*\n)(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n|\|$))+)',
        "name": "table",
        "priority": 80,
        "left": "|",
        "right": "",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": TableBlockifier,
    },
    {
        "pattern": r'(?:(?:^\>\s+)(\{(?P<attrs>.*?)\})?\s*(?:\n))?(?P<content>(?:\>\s+.*(?:\n|$))+)',
        "name": "blockquote",
        "priority": 90,
        "left": "> ",
        "right": "",
        "singleline": False,
        "nested": True,
        "nestedpriority": 1,
        "class": BlockquoteBlockifier,
    },
    {
        "pattern": r'\n\*\*\*\n',
        "name": "hr",
        "priority": 100,
        "left": "***",
        "right": "",
        "singleline": True,
        "nested": False,
        "nestedpriority": 0,
        "class": HRBlockifier,
    },
    {
        "pattern": r'^(?P<level>#{1,6})\s*(?P<content>.*?)(?:\{(?P<attrs>.*?)\})?\s*(?:\n|$)',
        "name": "heading",
        "priority": 110,
        "left": "#",
        "right": "",
        "singleline": True,
        "nested": False,
        "nestedpriority": 0,
        "class": HeadingBlockifier,
    },
    {
        "pattern": r'!\[(?P<attrs>.*?)\]\((?P<content>.*?)\)',
        "name": "image",
        "priority": 120,
        "left": "![",
        "right": "",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": ImageBlockifier,
    },
    {
        "pattern": r'\<svg(?P<attrs>.*?)\>(?P<content>.*?)\<\/svg\>',
        "name": "svg",
        "priority": 130,
        "left": "<svg",
        "right": "",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": SVGBlockifier,
    },
    {
        "pattern": r'(?P<content>(?:.*(?:\n|$))+)',
        "name": "paragraph",
        "priority": 140,
        "left": "",
        "right": "",
        "singleline": False,
        "nested": False,
        "nestedpriority": 0,
        "class": ParagraphBlockifier,
    },
]