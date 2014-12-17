import pyparsing as pp
from funcy import first, tap

from dpath import (
    select_all_children,
    select_children,
    select_all_descendants,
    compose_selectors,
    select_text,
    make_filter
)

ctx = {
    "text": select_text
}

start, stop = pp.StringStart(), pp.StringEnd()
sep = pp.Literal("/").suppress()
osep = pp.Optional(sep)


descendants = pp.Literal("**")
children    = pp.Literal("*")
element     = pp.Word(pp.alphanums + "-_")
func        = pp.Word(pp.alphas, pp.alphanums + "-_") + "()"


condition = pp.Forward()

segment = (descendants | children | func | element) + condition
path = osep + segment + pp.ZeroOrMore(sep + segment) + osep
condition << pp.Optional(
    pp.Literal("[").suppress() + path + pp.Literal("]").suppress()
)

def condition_action(txt, loc, toks):
    return make_filter(first(toks))

condition.setParseAction(condition_action)
parser = (start + path + stop)


descendants.setParseAction(lambda _: [select_all_descendants])
children.setParseAction(lambda _: [select_all_children])
element.setParseAction(lambda t: [select_children(lambda x: x.is_named(t[0]))])
func.setParseAction(lambda toks: [ ctx[toks[0]] ])
parser.setParseAction(lambda toks: [compose_selectors(*toks)])


def query(query, node):
    matcher = first(parser.parseString(query))
    return matcher(node)

try:
    from betterprint import pprint
except ImportError:
    from pprint import pprint

# print parser.parseString("a/s")
# print parser.parseString("a/s[g/f]")
# print parser.parseString("a/s")
# print parser.parseString("a/s")
