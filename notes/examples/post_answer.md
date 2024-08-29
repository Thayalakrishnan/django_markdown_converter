```
0 - meta --------------------
---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---
1 - heading --------------------
## Pargraphs
2 - paragraph --------------------
Pargraph 4 **eos** aperiam dolorem numquam quisquam [^1]. Cupiditate ==reprehenderit== beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus `code` voluptates _similique_. Aut maiores hic laudantium distinctio[^2]. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit^5^ ex aspernatur eius ~~consectetur~~ blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.
3 - heading --------------------
## Footnotes
4 - footnote --------------------
[^1]:
    Footnote 1.
5 - footnote --------------------
[^2]:
    Footnote 2 and some inline `code`.
    If we indent the paragraph we cant put as much content here as we would like.

    This is a multiline footnote. It also does not matter where we put the footnote definition!
6 - heading --------------------
## Image
7 - image --------------------
![ blocktype="image" subtype="still" title="Title for a basic image with a caption" alt="This is an example of a basic image in markdown with a caption" height="1080" width="1920" caption="This is an example of a caption being included with a basic image." ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image2.jpg)
8 - heading --------------------
## Code Block
9 - code --------------------
```{ language="python" filename="playerawards.py" }
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
10 - heading --------------------
## Table
11 - table --------------------
| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |
{ id="small-table" caption="small table of values" }
12 - heading --------------------
## Ordered List
13 - ordered list --------------------
1. Item 1
2. Item 2
3. Item 3

14 - ordered list --------------------
5. Item 1
6. Item 2
7. Item 3
    1. Indented Item 1
    2. Indented Item 2

15 - heading --------------------
## Unordered List
16 - unordered list --------------------
- Item 1
- Item 2
- Item 3

17 - unordered list --------------------
- Item 1
- Item 2
- Item 3
    - Indented Item 1
    - Indented Item 2

18 - heading --------------------
## Blockquote
19 - blockquote --------------------
> blockquote
> blockquote
{ cite="www.google.com" }
20 - blockquote --------------------
> Outside Quote
>
> > Inside Quote
>
21 - blockquote --------------------
>
> ## Blockquote heading
>
> A Paragraph is the default element. How about some **inline markdown**?
>
> - list item 1
> - list item 2
> - list item 3
>
{ cite="www.google.com" }
22 - heading --------------------
## Admonition
23 - admonition --------------------
!!! note "Note Title"
    this is an admonition.
24 - admonition --------------------
!!! tip "Tip Title"
    for tips and tricks.

    multiline admontion.
25 - admonition --------------------
!!! tip "Tip Title"
    for tips and tricks.

    multiline admontion.

    ```python
    for i in range(5):
        print(i)
    ```
26 - admonition --------------------
!!! question
    further ideas, further links etc.
27 - heading --------------------
## Definition Lists
28 - definition list --------------------
: First Term
: This is the definition of the first term.
29 - definition list --------------------
: Second Term
: This is one definition of the second term.
30 - heading --------------------
## Paragraph with links
31 - paragraph --------------------
To include a link, we place the link text in brackets and immediately follow it with the link text in parentheses like [this link](https://lawen.thayalakrishnan.com) to the homepage! We can emphasise **[the link](https://lawen.thayalakrishnan.com)** by enclosing the markdown in double asterisks. The same applies to single asterisk to italise [the link](https://lawen.thayalakrishnan.com). Use angle brackets, to render the link raw <https://lawen.thayalakrishnan.com>. This is an email address <example@email.com> in the middle of a paragraph!

```