import unittest

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


from parser import query


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {"a": [3,4,5, {"z": 10}], "z": "zz"},
            {"b": "uj", "a": {"z": "az"}, "z": "zz"},
            ["argh", "asssert", "so", "on"],
        ]

        self.test_paths = [
            "0/a/**",
            "**/a/*",
            "**/z",
            "1",
            "/1/a/z"
        ]

        self.tree = nodify("root", self.test_data)


    def test_simple_paths(self):
        for path in self.test_paths:
            pprint([path, query(path, self.tree).as_json()])

    def test_simple_compose(self):
        res = compose_selectors(
            select_all_descendants,
            select_children(lambda x: x.named("a")),
            select_all_children
        )(self.tree).as_json()

        res2 = query("**/a/*", self.tree).as_json()
        self.assertEqual(res, res2)

    def test_simple_mapper(self):
        pprint(
            compose_selectors(select_all_descendants,
                              make_mapper(lambda x: x.val if is_leaf(x) else []))

            (self.tree))

    def test_text_selector(self):
        import json
        selector = compose_selectors(
            select_all_descendants,
            make_filter(lambda x: x.named("set-cookie")),
            select_text
        )
        b = nodify("root", json.load(open("../sample3.json")))
        self.assertEqual(selector(b), query("**/set-cookie/text()", b))



if __name__ == '__main__':
    unittest.main()
