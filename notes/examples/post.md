---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---
{ blocktype="meta" }

## Pargraphs
{ blocktype="heading" }

Pargraph 4 **eos** aperiam dolorem numquam quisquam [^1]. Cupiditate ==reprehenderit== beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus `code` voluptates _similique_. Aut maiores hic laudantium distinctio[^2]. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit^5^ ex aspernatur eius ~~consectetur~~ blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.
{ blocktype="paragraph" }

To include a link, we place the link text in brackets and immediately follow it with the link text in parentheses like [this link](https://lawen.thayalakrishnan.com) to the homepage! We can emphasise **[the link](https://lawen.thayalakrishnan.com)** by enclosing the markdown in double asterisks. The same applies to single asterisk to italise [the link](https://lawen.thayalakrishnan.com). Use angle brackets, to render the link raw <https://lawen.thayalakrishnan.com>. This is an email address <example@email.com> in the middle of a paragraph!
{ blocktype="paragraph" }

## Image
{ blocktype="heading" }

![ This is an example of a basic image in markdown with a caption ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image2.jpg "Title for a basic image with a caption")
{ blocktype="image" subtype="still" height="1080" width="1920" caption="This is an example of a caption being included with a basic image." }


## Code Block
{ blocktype="heading" }

```python
from nba_api.stats.endpoints import playerawards as pa
```
{ blocktype="code" filename="playerawards.py" }

```
from nba_api.stats.endpoints import playerawards as pa
```
{ blocktype="code" }

```python
from nba_api.stats.endpoints import playerawards as pa

def DataReturn(dataset):
    headers, data = dataset["headers"], dataset["data"]
    if (len(data) == 0):            # no return value
        print('No Values')
        return []
    elif (len( data ) == 1):        # one row
        return data[0]
    else:                           # multiple rows
        return data

def getPlayerAccolades(player_id):
    player = pa.PlayerAwards(player_id=player_id).player_awards
    return DataReturn(player.get_dict())

def CreateCounter(dataset, position):
    values = [_[position] for _ in dataset]
    dict_counter = dict.fromkeys(set(values), 0)
    [dict_counter[_] + 1 for _ in values]
    print(dict_counter)
    return dict_counter
```
{ blocktype="code" language="python" }

```md
> blockquote
> blockquote

> Outside Quote
>
> > Inside Quote
>
```
{ blocktype="code" }

## Line break
{ blocktype="heading" }

---
{ blocktype="hr" }

***
{ blocktype="hr" }

## Table
{ blocktype="heading" }

| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |
{ blocktype="table" id="small-table" caption="small table of values" }


| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |
{ blocktype="table" id="small-table" caption="small table of values" }

## Blockquote
{ blocktype="heading" }

> blockquote
> blockquote
{ blocktype="blockquote" cite="www.google.com" }

> Outside Quote
>
> > Inside Quote
>
{ blocktype="blockquote" cite="www.google.com" }

> ## Blockquote heading
> { blocktype="heading" }
>
> A Paragraph is the default element. How about some **inline markdown**?
>
> - list item 1
> - list item 2
> - list item 3
{ blocktype="blockquote" cite="www.google.com" }


>
> > ## Blockquote heading
> > { blocktype="heading" }
> >
> > A Paragraph is the default element. How about some **inline markdown**?
> >
> > A second nested block in a blockquote with some **inline markdown**?
> >
> > - list item 1
> > - list item 2
> > - list item 3
>
{ blocktype="blockquote" cite="www.google.com" }

## Ordered List
{ blocktype="heading" }

1. Item 1
2. Item 2
3. Item 3
4. Item 4
{ blocktype="o list" }

1. Item 1
2. Item 2
3. Item 3
    1. Indented Item 1
    2. Indented Item 2
4. Item 4
{ blocktype="o list" }

1. Multiline Item 1, line 1.
   Multiline Item 1, line 2.
   
   Multiline Item 1, line 3 after double line break.
2. Item 2
3. Item 3
4. Item 4
{ blocktype="o list" }

1. Item 1
2. Item 2
3. Item 3
    1. Multiline Item 3, Subitem 1, line 1.
       Multiline Item 3, Subitem 1, line 2.
       
       Multiline Item 3, Subitem 1, line 3.
    2. Indented Item 2
4. Item 4
{ blocktype="o list" }

## Unordered List
{ blocktype="heading" }

- Item 1
- Item 2
- Item 3
- Item 4
{ blocktype="u list" }

- Item 1
- Item 2
- Item 3
    - Indented Item 1
    - Indented Item 2
- Item 4
{ blocktype="u list" }

- Multiline Item 1, line 1.
  Multiline Item 1, line 2
   
  Multiline Item 1, line 3 after double line break
- Item 2
- Item 3
- Item 4
{ blocktype="u list" }

- Item 1
- Item 2
- Item 3
    - Multiline Item 3, Subitem 1, line 1.
      Multiline Item 3, Subitem 1, line 2.
       
      Multiline Item 3, Subitem 1, line 3.
    - Indented Item 2
- Item 4
{ blocktype="u list" }

## Admonition
{ blocktype="heading" }

!!! note "Note Title"
    this is an admonition.
{ blocktype="admonition" }

!!! tip "Tip Title"
    for tips and tricks.
    
    multiline admontion.
{ blocktype="admonition" }

!!! tip "Tip Title"
    for tips and tricks.
    
    multiline admontion.
    
    ```python
    for i in range(5):
        print(i)
    ```
{ blocktype="admonition" }


!!! top question
    further ideas, further links etc.
{ blocktype="admonition" }

## Definition Lists
{ blocktype="heading" }

First Term
: This is the definition of the first term.
{ blocktype="dl list" }

Second Term
: This is the first definition of the second term.
: This is the second definition of the second term.
{ blocktype="dl list" }

Third Term
: This is the first definition of the third term.
: This is the second definition of the third term.
{ blocktype="dl list" }

## Footnotes
{ blocktype="heading" }

[^1]:
    Footnote 1.
{ blocktype="footnote" }

[^2]:
    Footnote 2 and some inline `code`.
    If we indent the paragraph we cant put as much content here as we would like.
    
    This is a multiline footnote. It also does not matter where we put the footnote definition!
{ blocktype="footnote" }

[^3]:
    Footnote 3 and some inline `code`.
    If we indent the paragraph we cant put as much content here as we would like.
    
    This is a multiline footnote. It also does not matter where we put the footnote definition!
{ blocktype="footnote" }

## Done
{ blocktype="heading" }
