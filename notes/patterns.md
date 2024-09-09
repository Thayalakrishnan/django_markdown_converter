## structures
- fenced: opens and closes with the same pattern
  - code
  - meta
- consecutive items that have the same prefix, or prefix pattern
  - u list 
  - o list
  - table
  - blockquote
- opening and closing on new line
  - footnote
  - admonition
- opening with a pattern closing with a different pattern
  - heading
  - image
  - svg
  - hr
- combo
  - d list
- other
  - paragraph

## inline styling
- these elements can have inline styling
- paragraph, olist, u list, blockquote, footnote, admonition, heading, d list, table
## nested block level content
- these elements can have block level elements nested inside of their structure
  - olist, u list, blockquote, footnote, admonition

## attrs
```re
(?:\{.*?\})?
(?:\n\{.*?\})?
(?:\{.*?\})?
```
### rules

#### none
- meta
#### after
- unordered list
- ordered list
- definition list
- admonition
- footnote
- table
- blockquote
- hr
- paragraph

#### inline
- code
- heading
- image
- svg

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

## openers

```md
###
--- 
| 
- 
1. 
\`\`\`
!!!
[^
: 
> 
***
![
<svg
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

### meta
```re
^(?:---\s*)(?:\n)(?P<content>.*?)(?:---\s*)(?:\n|$)
# simple
^---.*?$.*?^---.*?$
^---.*?---$
```
props:
- 



### definition list
```re
\:\s+(?P<term>.+?)(?=\n{2}|$)\n\:\s+(?P<definition>.+?)(?=\n{2}|$)
(?:^.+?\n)(?:\: .*?\n)+(?!\:\n)
^.+?$(?:\n\: .*?$)+(?:\n\{.*?\})?
^.+?$\n(?:\: .*?$\n)+(?:\{.*?\}\n)?
```
props:
- attrs
- term
- definition

### footnote
```re
\[\^(?P<index>.+?)\]:\s*\n(?P<content>(?: {4,}.*(?:\n|$))+)
# simple
(?:^\[\^.+?\]:.*?$)(?:.*?)(?:\n\n|\n$)
```
props:
- attrs

### admonition
```re
!!!\s+(?P<type>[a-zA-Z]+)?\s*(?:\s+["\'](?P<title>[^"\']+?)["\'])?\s*\n(?P<between>(?: {4,}.*(?:\n|$))+)
# simple
(?:^!!!.*?$)(?:.*?)(?:\n$|\n\n)
(?:^!!!.*?\n)(?:.*?\n)+?(?=^\n) # multiline
(?:^!!!.*?$)(?:.*?)(?=^\n) # multiline, dotall

```
props:
- attrs
- type
- title

### code
```re
^```.*?\n(?P<between>.*?)(?<=\n)(?:```)\s*$

## simple
^```.*?```\s*?$
## complex
```
props:
- attrs
- language


### table
```re
# simple
(?:^\|.*?\|$)+?(?!\n\|)
(?:^\|.*?\| *?$)+?(?!\n\|)

## Flags: multiline
(?:^\|.*?\|\s*?\n)+(?!\n\|) 
(?:^\|.*?\|\s*?\n)+(?:$)
(?:^\|.*?\|\s*?$\n?)+

# complex 
## Flags: multiline, dotall
^(?P<header>\|.*?\|\n)(?P<break>\|.*?\|\n)(?P<body>\|.*?\|(\n|$)){1,}(?:\{(?P<attrs>.*?)\})? 
```
props:
- attrs
- header
- body
- footer

### blockquote
```re
# simple
## Flags: multiline
(?:>.*?\n)+(?!>\n)
(?:>.*?\n)+(?!>\n)(?:\{.*?\})?
(?:^>\s+?.*?$\n)+
(?:^>\s+?.*?$\n)+(?:\{.*?\})?

(?:^>\s+?.*?$\n)+(?=\n)

```
props:
- attrs
- citation


### unordered list
```re
(?:-\s+?.*?$\n)(?:^\s*?-\s+?.*?$\n)+(?!^\s*?-\s+?.*?$\n)
(?:^-\s.*?$\n)(?:^\s*?-\s.*?$\n)+


(?:^-\s+.*$)
(?:^(?:-\s+.*)\n)(?:^(?:\s*-\s+.*)\n)+(?:\n$)

(?:^ *- +.*?\n)+(?=$\n)

# simple
## flags: multiline, dotall
(?:^ *[\-\*\+] +.*?\n)+(?=\n)
```
props:
- attrs

### ordered list
```re

# simple
(^ *\d+\. +.*?$\n)+(?=\n)
```
props:
- attrs

### paragraph
```re
```
props:
- attrs

### hr
```re
```
props:
- attrs


### heading
```re
```
props:
- attrs
- level


### image
```re
```
props:
- attrs
- subtype

### svg
```re
```
props:
- attrs


