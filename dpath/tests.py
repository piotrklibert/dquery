try:
    from betterprint import pprint
except ImportError:
    from pprint import pprint

from dpath import (
    nodify,
    compose_selectors,
    select_all_descendants,
    make_filter,
    make_mapper,
    select_children,
    select_text,
    is_leaf,
    select_all_children
)

test_data = [
    {"a": [3,4,5, {"z": 10}], "z": "zz"},
    {"b": "uj", "a": {"z": "az"}, "z": "zz"},
    ["argh", "asssert", "so", "on"],
]

test_paths = [
    "0/a/**",
    "**/a/*",
    "**/z",
    "1",
    "/1/a/z"
]

tree = nodify("root", test_data)

from parser import query

for path in test_paths:
    pprint([path, query(path, tree).as_json()])

res = compose_selectors(
    select_all_descendants,
    select_children(lambda x: x.named("a")),
    select_all_children
)(tree).as_json()

res2 = query("**/a/*", tree).as_json()
print res == res2

pprint(
    compose_selectors(select_all_descendants,
                      make_mapper(lambda x: x.val if is_leaf(x) else []))

    (tree))




import json
b = nodify("root", json.load(open("../sample3.json")))
bb = compose_selectors(
    select_all_descendants,
    make_filter(lambda x: x.named("set-cookie")),
    select_text
)(b)


pprint(bb)
