## base structure 
```
r"pattern=r'^@@@\s*(?:\{(?P<attrs>.*?)\})?\s*\n(?P<content>.*?)\n\s*@@@\s*(?:\n\s*|$)',"
```

```
^
(?:\|\s*\{(?P<attrs>.*?)\}\s*\|\s*\n)
(?:\|(?P<header>.*?)\|\s*\n)
(?:\|(?P<settings>.*?)\|\s*\n)
(?P<content>.*?)
(?:\n\s*|$)


^(?:\|\s*\{(?P<attrs>.*?)\}\s*\|\s*\n)(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>.*?)(?:\n\s*|$)



## tyring to capture the attrs at the end

^
(?:\|(?P<header>.*?)\|\s*\n)
(?:\|(?P<settings>.*?)\|\s*\n)
(?P<content>(?:.*(?:\|\n))+)
(?:\|\s*\{(?P<attrs>.*?)\}\s*\|\s*\n)?
(?:\n\s*|$)

^(?:\|(?P<header>.*?)\|\s*\n)(?:\|(?P<settings>.*?)\|\s*\n)(?P<content>(?:.*(?:\|\n))+)(?:\s*\{(?P<attrs>.*?)\}\s*\n)?(?:\n\s*|$)


## tyring to capture the attrs at the end
^
(?:\|(?P<header>.*?)\|\s*\n)
(?:\|(?P<settings>.*?)\|\s*\n)
(?P<content>.*?)
(?:\{(?P<attrs>.*?)\})?
(?:\n\s*|$)

^
(?:\|(?P<header>.*?)\|\s*\n)
(?:\|(?P<settings>.*?)\|\s*\n)
(?P<content>.*?)

(?P<end>(?:\s*\{\s*(?P<attrs>.*?)\s*\}(?:\n\s*|$))|(?:\n\s*|$))

(?:\s*\{\s*(?P<attrs>.*?)\s*\}(?:\n\s*|$))|(?:\n\s*|$)
```


## regeex for list items

```regex

^
(?P<listitem>
    (?P<indentation>\s*)
    (?P<marker>.+?)\s+
    (?P<item>.+?)
    (?=\n{1}|$)
    (?P<rest>(?:\s{0,}.*(?:\n|$))+)?
)
(?:\n|$)
'


^
(?P<listitem>
    (?P<indentation>\s*)
    (?P<marker>.+?)\s+
    (?P<item>.+?)
    (?=\n{1}|$)
)
(?:\n|$)



^(?P<listitem>(?P<indentation>\s*)(?P<marker>.+?)\s+(?P<item>.+?)(?=\n{1}|$))+(?:\n|$)
'
```