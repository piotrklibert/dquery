## dQuery: XPath for querying nested data for Python

Uses funcy and pyparsing as dependencies.

There are some examples in `dpath/tests.py`

Basically:


```python

query(nodify([{"a": [3,4,5, {"z": 10}], "z": "zz"},
              {"b": "uj", "a": {"z": "az"}, "z": "zz"},
              ["argh", "asssert", "so", "on"],],
              "**/z"
              ).as_json() == ['zz', 10, 'zz', 'az'])
```
