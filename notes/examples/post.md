---
title: Markdown Test
author: Lawen Thayalakrishnan
tags: markdown, python, parser
---

## Paragraphs

### Basic Paragraphs

Voluptatem eos aperiam dolorem numquam quisquam. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus maxime voluptates similique. Aut maiores `Inline code` hic laudantium distinctio. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.

Voluptatem eos aperiam dolorem numquam quisquam. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus maxime voluptates similique. Aut maiores `Inline code` hic laudantium distinctio. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.

### paragraphs with inline markup

Eaque dolorum cumque minima asperiores voluptatum laborum provident. Esse suscipit adipisci debitis non voluptatum. Id accusamus optio iste similique cupiditate facere asperiores perspiciatis. Hic voluptatum neque ullam `Inline code` odio iste nam porro dolorum. Sit autem consequatur nam nisi totam possimus dolor quibusdam debitis. Quod adipisci sequi facere sunt error consectetur veritatis laboriosam sunt. Saepe iure ea quibusdam et iure aliquam ipsam `Inline code` soluta deserunt. Debitis maxime voluptatum similique. Sapiente fuga molestias expedita illo `Some longer inline code` sequi ea quo sed. Temporibus amet commodi quae esse repudiandae voluptatum labore officiis modi. Eaque dolorum cumque minima asperiores voluptatum laborum provident. Esse suscipit adipisci debitis non voluptatum. Id accusamus optio iste similique cupiditate facere --The world is flat-- Hic voluptatum neque ullam `Inline code` odio iste nam porro dolorum. Sit autem consequatur nam nisi totam possimus dolor quibusdam debitis. Quod adipisci sequi facere sunt error consectetur veritatis laboriosam sunt. Saepe iure ea quibusdam et iure aliquam ipsam `Inline code` soluta deserunt. Debitis maxime voluptatum similique. Sapiente fuga molestias expedita illo `Some longer inline code` sequi ea quo sed. Temporibus amet commodi quae esse repudiandae voluptatum labore officiis modi. This is some supersript X^2^ in the middle of a paragraph and then some super~script~ ! This is some *italicized text* in the middle of a paragraph! This is some **bold text** in the middle of a paragraph!

### paragraphs with footnotes

Voluptatem eos aperiam dolorem numquam quisquam [^1]. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus maxime voluptates similique. Aut maiores hic laudantium distinctio[^2]. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.

Voluptatem eos aperiam dolorem numquam quisquam. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus maxime voluptates similique. Aut maiores hic laudantium distinctio. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in [^3].

Voluptatem eos aperiam dolorem numquam quisquam. Cupiditate reprehenderit beatae ab inventore libero. Accusantium explicabo optio debitis magni sint earum excepturi. Dicta aliquid cupiditate. Consequuntur temporibus maxime voluptates similique. Aut maiores hic laudantium distinctio. Aliquid magni expedita voluptatem illo laudantium illo. Quidem occaecati voluptas odit ex aspernatur eius consectetur blanditiis [^4]. Aperiam ullam iure soluta animi voluptatem pariatur nesciunt voluptatibus. Fuga iste in.


[^1]:
    Footnote definition.

[^2]:
    Footnote definition and some inline `code`.

[^3]:
    Footnote definition.
    If we indent the paragraph we cant put as much content here as we would like.
    
    This is a multiline footnote. It also does not matter where we put the footnote definition!

[^4]:
    Footnote definition.

## Images

### basic image

![ blocktype="image" subtype="still" title="Title for a basic image" alt="This is an example of a basic image in markdown" height="1080" width="1920" caption="Gif demonstrating the GUIs live plotting ability." ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image1.jpg)

### basic image with caption

![ blocktype="image" subtype="still" title="Title for a basic image with a caption" alt="This is an example of a basic image in markdown with a caption" height="1080" width="1920" caption="This is an example of a caption being included with a basic image." ](https://thayalakrishnan-lawen-prod-media.s3.ap-southeast-2.amazonaws.com/media/images/covers/image2.jpg)

### animated image with caption

![ blocktype="image" subtype="animated" title="Title for a animated image with a caption" alt="This is an example of a animated image in markdown with a caption" height="1080" width="1920" caption="This is an example of a caption being included with an animated image." ](https://thayalakrishnan-lawen-prod-media.s3.amazonaws.com/media/images/demogifs/sphere_plot_full.webp)

### SVG Image

![ blocktype="image" subtype="still" title="A high level overview of the data flow through this website." alt="This figure depicts, at a high level, the data flow of this website." height="1920" width="1080" caption="A high level overview of the data flow through this website." ](https://thayalakrishnan-lawen-prod-media.s3.amazonaws.com/media/markdownx/2023/03/01/5cb0f16b-34d8-4f6d-9c18-bfaad2eec2bb.svg)


## Code Blocks

### Code Block

```{ language="python" filename="main.py"}
for i in range(20):
    print(i)
```

### Large Code Block

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

### Code Block With Caption

## Tables

### Small Table

| { id="small-table" caption="small table of values" } |
| Column 1 Title | Column 2 Title |
| ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 |
| Row 2 Column 1| Row 2 Column 2 |

### Big Table

| { id="big-table" caption="big table of values" } |
| Column 1 Title | Column 2 Title | Column 3 Title | Column 4 Title | Column 5 Title | Column 6 Title |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Row 1 Column 1| Row 1 Column 2 | Row 1 Column 3 | Row 1 Column 4 | Row 1 Column 5 | Row 1 Column 6 |
| Row 2 Column 1| Row 2 Column 2 | Row 2 Column 3 | Row 2 Column 4 | Row 2 Column 5 | Row 2 Column 6 |
| Row 3 Column 1| Row 3 Column 2 | Row 3 Column 3 | Row 3 Column 4 | Row 3 Column 5 | Row 3 Column 6 |
| Row 4 Column 1| Row 4 Column 2 | Row 4 Column 3 | Row 4 Column 4 | Row 4 Column 5 | Row 4 Column 6 |
| Row 5 Column 1| Row 5 Column 2 | Row 5 Column 3 | Row 5 Column 4 | Row 5 Column 5 | Row 5 Column 6 |

## Markdown lists

### Ordered List

1. Item 1
2. Item 2
3. Item 3
4. Item 4

### nested ordered lists

1. Item 1
2. Item 2
3. Item 3
    1. Indented Item 1
    2. Indented Item 2
4. Item 4

### Unordered List

- Item 1
- Item 2
- Item 3
- Item 4

### nested unordered lists

- Item 1
- Item 2
- Item 3
    - Indented Item 1
    - Indented Item 2
- Item 4

## Blockquotes

### blockquote

> blockquote

> { cite="www.google.com" }
> blockquote
> blockquote

### Nested Blockquote

> Outside Quote
>
> > Inside Quote
>

### blockquotes with other markdown

> { cite="www.google.com" }
>
> ## Blockquote with markdown
>
> A Paragraph is the default element. How about some **inline markdown**?
>
> - list item 1
> - list item 2
> - list item 3
>


## Admonitions

### With Title

!!! note "Note Title"
    this is an admonition.

!!! warning "Warning Title"
    For warnings.

!!! important "Important Title"
    For important info.

!!! caution "Caution Title"
    for cautioning.

!!! tip "Tip Title"
    for tips and tricks.
    
    multiline admontion.

### Without Title

!!! question
    further ideas, further links etc.

!!! quote
    extracts from the text.

!!! comment
    comments or opinions.

!!! docs
    Manuals, listings, diagrams, graphics etc.
    
    multiline admontion.

## Definition Lists

: First Term
: This is the definition of the first term.

: Second Term
: This is one definition of the second term.
: This is another definition of the second term.

## Link Handling

### paragraph with links

To include a link, we place the link text in brackets and immediately follow it with the link text in parentheses like [this link](https://lawen.thayalakrishnan.com) to the homepage! We can emphasise **[the link](https://lawen.thayalakrishnan.com)** by enclosing the markdown in double asterisks. The same applies to single asterisk to italise [the link](https://lawen.thayalakrishnan.com). Use angle brackets, to render the link raw <https://lawen.thayalakrishnan.com>. This is an email address <example@email.com> in the middle of a paragraph!
