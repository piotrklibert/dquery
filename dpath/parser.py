import pyparsing as pp
from funcy import first


from dpath import (
    select_children, select_all_children, select_all_descendants,
    compose_selectors, select_text, make_filter
)


ctx = {
    "text": select_text
}

start, stop = pp.StringStart(), pp.StringEnd()
sep         = pp.Literal("/").suppress()
osep        = pp.Optional(sep)


descendants = pp.Literal("**")
children    = pp.Literal("*")
element     = pp.Word(pp.alphanums + "-_")
func        = pp.Word(pp.alphas, pp.alphanums + "-_") + "()"


condition = pp.Forward()        # condition and path are mutually recursive

segment   = (descendants | children | func | element) + condition
path      = osep + segment + pp.ZeroOrMore(sep + segment) + osep

condition << pp.Optional(
    pp.Literal("[").suppress() + path + pp.Literal("]").suppress()
)


parser = (start + path + stop)


@condition.setParseAction
def condition_action(txt, loc, toks):
    return make_filter(first(toks))

@descendants.setParseAction
def descendants_action(txt, loc, toks):
    return [select_all_descendants]

@children.setParseAction
def children_action(txt, loc, toks):
    return [select_all_children]

@element.setParseAction
def element_action(txt, loc, toks):
    return [select_children(lambda x: x.is_named(toks[0]))]

@func.setParseAction
def func_action(txt, loc, toks):
    return [ctx[toks[0]] ]

@parser.setParseAction
def parser_action(txt, loc, toks):
    return [compose_selectors(*toks)]


def query(query, node):
    matcher = first(parser.parseString(query))
    return matcher(node)
