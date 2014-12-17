## dQuery: XPath for querying nested data for Python

Uses funcy and pyparsing as dependencies.

There are some examples in `dpath/tests.py`


API is very fluid right now, but the general idea is like this:


```python
data = [
    {"a": [3, 4, 5, {"z": 10}], "z": "zz"},
    {"b": "uj", "a": {"z": "az"}, "z": "zz"},
    ["argh", "asssert", "so", "on"],
]

assert query(data, "**/z") == ['zz', 10, 'zz', 'az']
```
