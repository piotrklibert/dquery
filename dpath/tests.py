import unittest


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
            [path, query(path, self.tree).as_json()]


    def test_simple_compose(self):
        _selector = compose_selectors(
            select_all_descendants,
            select_children(lambda x: x.is_named("a")),
            select_all_children
        )

        self.assertEqual(
            _selector(self.tree).as_json(),
            query("**/a/*", self.tree).as_json(),
        )


    def test_simple_mapper(self):
        _mapper = compose_selectors(
            select_all_descendants,
            make_mapper(lambda x: x.val if is_leaf(x) else None)
        )
        self.assertEquals(len(_mapper(self.tree)), 19)


    def test_text_selector(self):
        import json
        _selector = compose_selectors(
            select_all_descendants,
            make_filter(lambda x: x.is_named("set-cookie")),
            select_text
        )
        b = nodify("root", json.load(open("../sample3.json")))
        self.assertEqual(_selector(b), query("**/set-cookie/text()", b))


    def test_conditional(self):
        nodes = query("**[z]", self.tree).as_json()
        self.assertEquals(len(nodes), 4)

        nodes = query("*[a]", self.tree)
        self.assertEquals(len(nodes.as_json()), 2)


if __name__ == '__main__':
    unittest.main()
