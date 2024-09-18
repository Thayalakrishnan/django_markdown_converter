## copyandpaste

```python
def revert(self, *args, **kwargs) -> str:
    block = super().revert(*args, **kwargs)
    
    props = block.get("props", {})
    data = block.get("data", "")
    
    ret = []
    ret.extend(data)
    ret.append(f"")
    return "\n".join(ret)
```

## General
- props which aren't apart of the blocks personal props, should be processed and returned as 
  - attrs placed at the end of the block


- for nested content, i think i need to loop over them until they are all flattened from the inside out it seems
## META_PATTERN

### input

```json
{
    "type": "meta",
    "props": {},
    "data": {
        "key1": "value 1",
        "key2": "value 2",
    },
}
```

### transform

```python
ret = ["---"]
middle = [f"{key}: {block[key]}" for key in block]
ret.extend(middle)
ret.append("---")
out = "\n".join(ret)
```

### output

```md
---
key1: value 1
key2: value 2
---
```

## CODE_PATTERN

### input

```json
{
    "type": "code",
    "props": {
        "language": "python"
    },
    "data": [
        [["k","for"],["w"," "],["n","i"],["w"," "],["ow","in"],["w"," "],["nb","range"],["p","("],["mi","5"],["p",")"],["p",":"]],
        [["w","    "],["nb","print"],["p","("],["n","i"],["p",")"]]
    ],
}
```

### transform

```python
ret = []
ret.append(f"```{block.get('language', '')}")
middle = []
for row in block["data"]:
    line = "".join(list(map(lambda x: x[1], row)))
    middle.append(line)
ret.extend(middle)
ret.append(f"```")
out = "\n".join(ret)
```

### output

```md
```python
for i in range(5):
    print(i)
```

## DLIST_PATTERN

### input

```json
{
    "type": "dlist",
    "props": {},
    "data": {
        "term": "",
        "definition": [
            "definition 1",
            "definition 2",
        ],
    },
}
```

### transform

```python
term = block["data"].get("term")
definition = block["data"].get("definition")
definition = [f": {_}" for _ in definition]

ret = []
ret.append(term)
ret.extend(definition)
out = "\n".join(ret)
```

### output

```md
term
: definition 1
: definition 2
```

## FOOTNOTE_PATTERN

### input

```json
{
    "type": "footnote",
    "props": {
        "index": 1
    },
    "data": "Content for footnote",
}
```

### transform

```python
index = block["props"].get("index")
data = block["data"]
data = [f"    {_}" for _ in data.splitlines()]
ret = []
ret.append(f"[^{index}]:")
ret.extend(data)
out = "\n".join(ret)
```

### output

```md
[^1]:
    Content for footnote
```

## ADMONITION_PATTERN

### input

```json
{
    "type": "admonition",
    "props": {
        "type": "note",
        "title": "Example Admonition",
    },
    "data": "Content for the admonition",
}
```

### transform

```python
atype = f' {block["props"].get("type", "")}'.rstrip()
title = f' {block["props"].get("title", "")}'.rstrip()
data = block["data"]

data = [f"    {_}" for _ in data.splitlines()]
ret = []
ret.append(f"!!!{atype}{title}")
ret.extend(data)
out = "\n".join(ret)
```

### output

```md
!!! note "Example Admonition"
    Content for the admonition.
```

## TABLE_PATTERN

### input

```json
{
    "type": "table",
    "props": {},
    "data": {
        "header": ["header 1", "header 2"],
        "body": [
            ["row 1 col 1", "row 1 col 2"],
            ["row 2 col 1", "row 2 col 2"],
        ]
    },
}
```

### transform

```python

create_row_lambda = lambda x: f"| {' | '.join(x)} |"
ret = []

header = block["data"].get("header")
body = block["data"].get("body")
breaker = ['---']*len(header)

ret.append(create_row_lambda(header))
ret.append(create_row_lambda(breaker))
for row in body:
    ret.append(create_row_lambda(row))
out = "\n".join(ret)
```

### output

```md
| header 1 | header 2 |
| --- | --- |
| row 1 col 1 | row 1 col 2 |
| row 2 col 1 | row 2 col 2 |
```

## HR_PATTERN

### input

```json
{
    "type": "hr",
    "props": {},
    "data": "---",
}
```

### transform

```python
ret = [block["data"]]
ret.append("")
out = "\n".join(ret)
```

### output

```md
---
```

## HEADING_PATTERN

### input

```json
{
    "type": "heading",
    "props": {
        "index": 1
    },
    "data": "Example Heading",
}
```

### transform

```python
create_heading_lambda = lambda lvl, txt: f"{'#'*lvl} {txt}"
level = block["props"].get("level", 1)
data = block["data"]

ret.append(create_heading_lambda(level, data))
ret.append("")
out = "\n".join(ret)
```

### output

```md
# Example Heading
```

## IMAGE_PATTERN

### input

```json
{
    "type": "image",
    "props": {
        "title": "Title for image",
        "alt": "Alt texgt for image",
    },
    "data": "https://picsum.photos/1920/1080",
}
```

### transform

```python
create_image_lambda = lambda a, s, t: f"![{a}]({s} \"{t}\")" if len(t) else f"![{a}]({s})"

alt = block["props"].get("alt", "")
src = block.get("data", "")
title = block["props"].get("title", "")

ret = []
ret.append(create_image_lambda(alt, src, title))
ret.append("")
out = "\n".join(ret)
```

### output

```md
![ Alt texgt for image ](https://picsum.photos/1920/1080 "Alt texgt for image")
```

## SVG_PATTERN

### input

```json
{
    "type": "svg",
    "props": {
        "height": "100",
        "width": "100"
    },
    "data": "<rect x=\"25\" y=\"25\" height=\"50\" width=\"50\"></rect>"
}
```

### transform

```python
generate_attrs = lambda k,v: f'{k}="{v}"'
pad_if_present = lambda x: f' {x}' if len(x) else f''
wrap_html_content = lambda t, a, c: f'<{t}{pad_if_present(a)}>{c}</{t}>'

props = block.get("props", {})
attrs = " ".join(list(map(generate_attrs, zip(props.keys(), props.values()))))

data = block.get("data", "")

ret = []
ret.append(wrap_html_content("svg", attrs, data))
ret.append("")
out = "\n".join(ret)
```
### output

```md
<svg height="50" width="50"><rect x="25" y="25" height="50" width="50"></rect></svg>
```

## LIST_PATTERN

### input

```json
{
    "type": "list",
    "props": {},
    "data": "",
}
```

### transform

```python
blocktype = block.get("type", "ulist")
props = block.get("type", {})
data = block.get("data", [])


if blocktype == "ulist":
    data = [f"- {_}" for _ in data]
else:
    data = [f"{i}. {_}" for i, _ in enumerate(data)]

ret = []
ret.extend(data)
out = "\n".join(ret)
```

### output

```md

```

## BLOCKQUOTE_PATTERN

### input

```json
{
    "type": "blockquote",
    "props": {},
    "data": "this is a blockquote",
}
```

### transform

```python

data = block.get("data", "")
data = [f"> {_}" for _ in data.splitlines()]

ret = []
ret.extend(data)
out = "\n".join(ret)
```

### output

```md
> this is a blockquote
```

## PARAGRAPH_PATTERN

### input

```json
{
    "type": "paragraph",
    "props": {},
    "data": "This is a sentence. ",
}
```

### transform

```python
props = block.get("props")
data = block.get("data")
ret = []
ret.append(data)
ret.append("")
out = "\n".join(ret)

```

### output

```md
This is a sentence. 
```
