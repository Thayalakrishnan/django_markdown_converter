## basic

```
from nba_api.stats.endpoints import playerawards as pa
```

## basic with language

```python
from nba_api.stats.endpoints import playerawards as pa
```

## basic with props

```python
from nba_api.stats.endpoints import playerawards as pa
```
{ blocktype="code" filename="playerawards.py" }

## multiline

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
    return dict_counter
```

## with nested html or anything else that may get picked up

```md
> blockquote
> blockquote

> Outside Quote
>
> > Inside Quote
>
```
