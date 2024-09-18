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

```str
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
        [["nb","print"],["p","("],["n","i"],["p",")"]]
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

```str
```python
for i in range(5):
    print(i)
```
```

## DLIST_PATTERN

### input

```json
{
    "type": "dlist",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## FOOTNOTE_PATTERN

### input

```json
{
    "type": "footnote",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## ADMONITION_PATTERN

### input

```json
{
    "type": "admonition",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## TABLE_PATTERN

### input

```json
{
    "type": "table",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## HR_PATTERN

### input

```json
{
    "type": "hr",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## HEADING_PATTERN

### input

```json
{
    "type": "heading",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## IMAGE_PATTERN

### input

```json
{
    "type": "image",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## SVG_PATTERN

### input

```json
{
    "type": "svg",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

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
lambda x:
f"{}"
```

### output

```str

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
lambda x:
f"{}"
```

### output

```str

```

## BLOCKQUOTE_PATTERN

### input

```json
{
    "type": "blockquote",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## PARAGRAPH_PATTERN

### input

```json
{
    "type": "paragraph",
    "props": {},
    "data": "",
}
```

### transform

```python
lambda x:
f"{}"
```

### output

```str

```

## 
