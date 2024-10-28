---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---
{ blocktype="meta" }

## Pargraphs

Pargraph 1 **eos** aperiam dolorem numquam quisquam [^1]. Cupiditate ==reprehenderit== beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus `code` voluptates _similique_. Aut maiores hic laudantium distinctio[^2]. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit^5^ ex aspernatur eius ~~consectetur~~ blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in. To include a link, we place the link text in brackets and immediately follow it with the link text in parentheses like [this link](https://lawen.thayalakrishnan.com) to the homepage! We can emphasise **[the link](https://lawen.thayalakrishnan.com)** by enclosing the markdown in double asterisks. The same applies to single asterisk to italise [the link](https://lawen.thayalakrishnan.com). Use angle brackets, to render the link raw <https://lawen.thayalakrishnan.com>. This is an email address <example@email.com> in the middle of a paragraph!

## Image

![ This is an example of a basic image in markdown with a caption ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image2.jpg "Title for a basic image with a caption")

## Code Block

```python
from nba_api.stats.endpoints import playerawards as pa

for i in range(5):
    print(i)
```

## Line break

---

## Table

| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| `Row 1 Column 1` | Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |

## Blockquote

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

## Lists

1. Item 1 line 1.
2. Item 2 line 1.
3. Item 3 line 1.
4. Item 4 line 1.

## Unordered List

- Item 1 line 1.
- Item 1 line 2.
  
  Item 1 line 3.
- Item 2 line 1.
- Item 3 line 1.
  - Item 3.1 line 1.
    Item 3.1 line 2.
    
    Item 3.1 line 3.
      - Item 3.1.1 line 1.
        Item 3.1.1 line 2.
        
        Item 3.1.1 line 3.
      - Item 3.1.2 line 1.
        Item 3.1.2 line 2.
        
        ```python
        for p in range(3):
            print(p)
        ```
        
        Item 3.1.2 line 3.
      - Item 3.1.3 line 1.
  - Item 3.2 line 1.
  - Item 3.3 line 1.
- Item 4

## Admonition

!!! tip "Tip Title"
    Line 1.
    Line 2.
    
    ```python
    for i in range(5):
        print(i)
    ```
    
    Line 3.

## Definition Lists

Second Term
: This is the first definition of the second term.
: This is the second definition of the second term.

## Footnotes

[^1]:
    Footnote 1. If we indent the paragraph we cant put as much content here as we would like.
    
    This is a multiline footnote. It also does not matter where we put the footnote definition!

## Done

