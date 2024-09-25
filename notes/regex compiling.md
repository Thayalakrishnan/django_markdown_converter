
using compile and re.escape from the regex library

```python
import re

pattern1 = re.compile(r'(?:\_\_)')
pattern2 = re.compile(r'(?:__)')
pattern3 = re.compile(re.escape(r'(?:__)'))

#print(pattern1.pattern)
#print(pattern2.pattern)
#print(pattern3.pattern)

pattern1 = f'(?:**)'
pattern2 = r'(?:**)'
pattern3 = f'(?:\*\*)'
pattern4 = r'(?:\*\*)'
pattern5 = re.escape(pattern1)
pattern6 = re.escape(pattern2)
pattern7 = re.escape(pattern3)
pattern8 = re.escape(pattern4)
pattern9 = r'(?:' + re.escape("**") + r')'
pattern10 = f'(?:{re.escape("**")})'

print(repr(pattern1)) #  '(?:**)' | f string
print(repr(pattern2)) #  '(?:**)' | raw string
print(repr(pattern3)) #  '(?:\\*\\*)' | f string with escaped characters
print(repr(pattern4)) #  '(?:\\*\\*)' | raw string with escaped characters
print(repr(pattern5)) #  '\\(\\?:\\*\\*\\)' | re.escaped f string
print(repr(pattern6)) #  '\\(\\?:\\*\\*\\)' | re.escaped raw string
print(repr(pattern7)) #  '\\(\\?:\\\\\\*\\\\\\*\\)' | re.escaped raw string
print(repr(pattern8)) #  '\\(\\?:\\\\\\*\\\\\\*\\)' | re.escaped raw string
print(repr(pattern9)) #  '(?:\\*\\*)' |
print(repr(pattern10)) # '(?:\\*\\*)' |

print(pattern1) # (?:**) | f string
print(pattern2) # (?:**) | raw string
print(pattern3) # (?:\*\*) | f string with escaped characters
print(pattern4) # (?:\*\*) | raw string with escaped characters
print(pattern5) # \(\?:\*\*\) | re.escaped f string
print(pattern6) # \(\?:\*\*\) | re.escaped raw string
print(pattern7) # \(\?:\\\*\\\*\) | re.escaped raw string
print(pattern8) # \(\?:\\\*\\\*\) | re.escaped raw string
print(pattern9) # (?:\*\*) |
print(pattern10) # (?:\*\*) |


## repr returns the canonical representation of the string
## it escapes characters so that they can be printed on stdout

```