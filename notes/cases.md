## structural cases

### only formating context preset

**formatted content**




## Basic Cases:

##  Nested Cases:
### Italic within Bold:
**bold *italic*** → <strong>bold <em>italic</em></strong>
**bold *italic* more bold** → <strong>bold <em>italic</em> more bold</strong>
**bold *italic** bold → <strong>bold <em>italic</em></strong> bold

### Bold within Italic:
*italic **bold*** → <em>italic <strong>bold</strong></em>
*italic **bold** more italic* → <em>italic <strong>bold</strong> more italic</em>
*italic **bold* italic → <em>italic <strong>bold</strong></em> italic

### Unbalanced Patterns:
*italic **bold → <em>italic **bold</em> (Unmatched bold)
**bold *italic → <strong>bold *italic</strong> (Unmatched italic)

## Complex Nesting Cases:
### Multiple Italics within Bold:
**bold *italic* bold *italic*** → <strong>bold <em>italic</em> bold <em>italic</em></strong>
### Multiple Bolds within Italic:
*italic **bold** italic **bold*** → <em>italic <strong>bold</strong> italic <strong>bold</strong></em>

### Deep Nesting of Italics and Bolds:
***bold and italic **more bold*** more italic* → <strong><em>bold and italic <strong>more bold</strong></em></strong> more italic
***italic and bold *nested italic** nested bold* → <strong><em>italic and bold <em>nested italic</em></strong> nested bold</em>

## Mixed and Overlapping Cases:
### Bold Overlapping with Italics:
***italic **bold*** → <em><strong>italic</strong></em> bold (depending on how Markdown is parsed, this may be treated as invalid/unbalanced)
*italic **bold** and more italic* → <em>italic <strong>bold</strong> and more italic</em>
**bold and *italic** more bold* → <strong>bold and <em>italic</em></strong> more bold
### Edge Cases:
*italic* **bold** → <em>italic</em> <strong>bold</strong> (separate, no nesting)
***bold and italic*** text → <strong><em>bold and italic</em></strong> text
Escaped Markdown: