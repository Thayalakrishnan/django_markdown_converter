## 08/09/2024
- there might be a fringe edge case where the meta keys are not all unique and 
  - an error is thrown when creating the dictionary from the tuples

## 06/09/2024
- there is a fringe case we need to look out for and that is attrs that may be present on a nested block level element. Say we have a code block that is nested within an admonition. 
  - maybe we should standardise our attrs to always be trailing and ensure that we folllow the normal trend for attrs 