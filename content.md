# Content management guide

This doc is in progress. I'm dumping the stuff here right now, will organize it later.

```
$ cat data/wiki.json | scripts/search.py -n "Akbar"
{
    "to": 1605,
    "from": 1542,
    "name": "Akbar",
    "type": ""
}
```

```
$ cat data/intermediate/pantheon.json | scripts/search.py -n "Akbar"
{
    "rating": 0.784730416875,
    "country": "Pakistan",
    "from": 1542,
    "name": "Akbar",
    "type": "politics"
}
```
