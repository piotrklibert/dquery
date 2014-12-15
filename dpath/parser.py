import pyparsing as pp
from funcy import first

from dpath import (
    select_all_children,
    select_children,
    select_all_descendants,
    compose_selectors,
    select_text
)

ctx = {
    "text": select_text
}

start, stop = pp.StringStart(), pp.StringEnd()
sep = pp.Literal("/").suppress()
osep = pp.Optional(sep)


descendants = pp.Literal("**")
children = pp.Literal("*")
element = pp.Word(pp.alphanums + "-_")
func = pp.Word(pp.alphas, pp.alphanums + "_") + pp.Literal("(") + pp.Literal(")")

condition = pp.Optional(pp.Literal("[") + pp.Literal("]"))

segment = (descendants | children | func | element) + condition

parser = (start + osep + segment + pp.ZeroOrMore(sep + segment) + osep + stop)


descendants.setParseAction(lambda _: [select_all_descendants])
children.setParseAction(lambda _: [select_all_children])
element.setParseAction(lambda t: [select_children(lambda x: x.named(t[0]))])
func.setParseAction(lambda toks: [ ctx[toks[0]] ])
parser.setParseAction(lambda toks: [compose_selectors(*toks)])


def query(query, node):
    matcher = first(parser.parseString(query))
    return matcher(node)
