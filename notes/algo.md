## current algo
- reset footnotes
- blockify the source content, create a list of blocks
  - create a list to add all the blokcs to
  - remove and replace `\r` characters
  - split the content into lines
  - ensure that there is a line break as the last few lines
  - find the blocks
    - loop over th elines and determines if a line is open
    - if the line is open, we keep looping over the lines until we find where the line closes
    - once we know where the line closes, we extract the content and process it as a block
    - we add the processed block into the blocklist
    - if theere are still lines left, we process them
    - go until all the lines in the list have been processed
- build the admonitions
- build the footnotes
  - if ther3e are footnotes attach to block list
- return the generated blocklist

## hig level algo

- receive the content
- process the content
  - ensure that the blocks are spaced out evenly
    - we can scan for newline characters that are fixed to the start of a line
    - this means that line is empty and is used for spacing
    - ideally we want a single line break character between our blocks
    - we also need to be aware of blocks that may have props
  - try and remove trailing whitespace
  - ensure that the content has newline characters at the end
- we are gonna loop over the content using regex iterators. 
  - the pattern will try and determine what a block is 
- our patterns are used to determine the correct block type for further processing
  - the initial patterns to use should be lightweight and generic. 
  - extract any props from the block
  - apply the secondary pattern to try and 