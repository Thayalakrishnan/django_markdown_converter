## attrs
```re
(?:\{.*?\})?
(?:\n\{.*?\})?
```


## table
```re
(?:^\|.*?\|\n){1,}
```


## blockquote
```re
(?:^>\s.*?\n$){1,}
(?:\>.*(?:\n\>.*)*)
(?:\>.*)(?:\n\>.*){1,}
```


```re
BLOCKQUOTE_BLOCK_DATA = r'(?P<content>(?:^>\s+.*?$){1,}(?:\n\n|\n$))'
HEADING_BLOCK_DATA = r'^(?P<content>(?P<level>\#{1,6})\s+(?P<text>.*?)(?:\{(?P<attrs>.*?)\})?\s*)(?:\n|$)'
IMAGE_BLOCK_DATA = r'(?P<content>!\[(?P<attrs>.*?)\]\((?P<src>.*?)\))'
SVG_BLOCK_DATA = r'(?P<content><svg\s(?P<attrs>[^>]*)>(?P<between>.*?)</svg>)'
ORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*\d+\.\s.*?\n){1,})'
UNORDERED_LIST_BLOCK_DATA = r'(?P<content>(\s*-\s.*?\n){1,})'
PARAGRAPH_BLOCK_DATA = r'(?P<content>.*?)(?:\n|\n\n|$)'
EXTRACT_ATTRS = r'(?P<before>.*)\{(?P<attrs>.*?)\}(?P<after>.*)'

```
