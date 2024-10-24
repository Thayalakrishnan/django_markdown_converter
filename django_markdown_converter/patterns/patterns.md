## No Nested
CODE_PATTERN: fenced, structured, leading line
META_PATTERN: fenced, structured
SVG_PATTERN: fenced, structured, leading line
IMAGE_PATTERN: structured
HR_PATTERN: 
TABLE_PATTERN: inline, structured, findall, leading line
HEADING_PATTERN: inline, prefixed, slightly structured
DLIST_PATTERN: inline, prefixed, findall, leading line

## Nested
FOOTNOTE_PATTERN: nested, indented, leading line
ADMONITION_PATTERN: nested,indented, leading line
ULIST_PATTERN: nested, prefixed, indented, findall
OLIST_PATTERN: nested, prefixed, indented, findall
BLOCKQUOTE_PATTERN: nested, prefixed, findall

## Inline Only
PARAGRAPH_PATTERN: inline

## nothing
NEWLINE_PATTERN
EMPTYLINE_PATTERN
NONE_PATTERN

## future
MATH_PATTERN: fenced, structured

## terms
- fenced: defined start and stop borders
- structured: content needs to be transformed speicifically eg: syntax highlighting, key value pairs etc
- inline: data contains inline markup that needs to be processed
- prefixed: content has a prefix that needs to be removed
- indented: content is indented, which needs to be removed
- findall: the data/content part is a repeatable structure that we should use findall for
- leading line: the block features a first line that is different to the rest of the content

## order of operations
- findall items
- remove fencing/prefix/indentaion
- convert structure
- convert content
- convert inline content

# conversion

## No Nested
CODE_PATTERN:
- language: 
- data: use language to convert data to tokens
META_PATTERN: fenced, structured
- data: convert data to key value pairs separated by a colon
SVG_PATTERN: fenced, structured
- data: leave as is or convert svg pattern to svg blocks
IMAGE_PATTERN:
- data: should be the src of the image. should be able to be hooked into whatever cloud storage solution we are using (AWS S3) or something
- alt: alt text. 
- title: title text
HR_PATTERN: 
- pass through
TABLE_PATTERN:
- use findall to find all the rows of the table
- process the structured content to return the header and the body
- loop over the cells and do inline markup conversion if possible
HEADING_PATTERN:
- process the heading to get the headings id 
- process inline conent
DLIST_PATTERN: inline, prefixed, findall
- term: straight
- definition: straight

## Nested
ADMONITION_PATTERN: nested,indented
- type: nothing
- title: remove quotations marks
- content: process nested content
FOOTNOTE_PATTERN: nested, indented
- grab the index for the footnote
- remove the indentation 
- create a sub block we can loop over and convert
ULIST_PATTERN: nested, prefixed, indented, findall
OLIST_PATTERN: nested, prefixed, indented, findall
- findall the list items
- remove the prefix and teh indentation
- add the items as children of the block
BLOCKQUOTE_PATTERN: nested, prefixed, findall
- findall the blockquote lines
- remove the prefix and join the content together to make a block
- re process the subblock to convert it

## Inline Only
PARAGRAPH_PATTERN: inline
- process inline conetnt