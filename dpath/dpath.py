from operator import attrgetter
from funcy import curry, all, compose, isa, complement, any_fn, filter

flip = lambda f: lambda a, b: f(b, a)


class Node(object):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def is_named(self, name):
        if all(isa(basestring), [self.name, name]):
            return self.name.lower() == name.lower()
        else:
            # most likely one of the arguments is an int - we get str from
            # the parser but the names (if numerical) are stored as ints
            return str(self.name) == str(name)

    def as_json(self):
        return self.val

    def as_node_set(self):
        return NodeSet(self)



class Branch(Node):
    """Branch is a kind of Node which may contain more Nodes as its value."""
    def __init__(self, name, children):
        self.name = name
        self.val  = NodeSet.from_seq(children)

    def as_json(self):
        is_array = compose(isa(int), attrgetter("name"))

        if all(is_array, self.children):
            return [x.as_json() for x in self.children]
        else:
            return {x.name:x.as_json() for x in self.children}

    @property
    def children(self):
        return self.val

    def __repr__(self):
        return "Branch(%s, #kids:%d)" % (self.name, len(self.children))


class Leaf(Node):
    def as_json(self):
        return self.val

    @property
    def children(self):
        return NodeSet()

    def __repr__(self):
        return "Leaf(%s, %s)" % (self.name, self.val)


is_branch = isa(Branch)
is_leaf   = isa(Leaf)



class NodeSet(list):
    @classmethod
    def from_seq(cls, seq):
        return cls(*seq)

    def __init__(self, *nodes):
        super(NodeSet, self).__init__(nodes)

    def append_or_extend(self, obj):
        if is_single(obj):
            self.append(obj)
        else:
            self.extend(obj)

    @property
    def children(self):
        return self

    def as_node_set(self):
        return self
    def as_json(self):
        return [node.as_json() for node in self]

is_nset = isa(NodeSet)
is_single = any_fn(is_leaf,
                   complement(isa(Node, NodeSet, list)))



def nodify(name, data):
    _nodify = lambda (name, data): nodify(name, data)
    if isinstance(data, list):
        return Branch(name, NodeSet.from_seq(map(_nodify, enumerate(data))))
    elif isinstance(data, dict):
        return Branch(name, NodeSet.from_seq(map(_nodify, data.iteritems())))
    else:
        return Leaf(name, data)


#   ____ ___  __  __ ____ ___ _   _    _  _____ ___  ____  ____
#  / ___/ _ \|  \/  | __ )_ _| \ | |  / \|_   _/ _ \|  _ \/ ___|
# | |  | | | | |\/| |  _ \| ||  \| | / _ \ | || | | | |_) \___ \
# | |__| |_| | |  | | |_) | || |\  |/ ___ \| || |_| |  _ < ___) |
#  \____\___/|_|  |_|____/___|_| \_/_/   \_\_| \___/|_| \_\____/
#

def map_union(proc, lst):
    res = NodeSet()
    for node in lst:
        res.append_or_extend(proc(node))
    return res


def nfilter(pred, nodes):
    return NodeSet.from_seq(filter(pred, nodes.as_node_set()))


make_filter = curry(nfilter)

def make_mapper(func):
    def _mapper(nodes):
        return map_union(func, nodes.as_node_set())
    return _mapper

def compose_selectors(*selectors):
    # compose_selectors(fn1, fn2) == lambda x: fn2(fn1(x))
    _compose = lambda f,g: lambda x: g(f(x))
    return reduce(_compose, selectors)



#  ____  _____ _     _____ ____ _____ ___  ____  ____
# / ___|| ____| |   | ____/ ___|_   _/ _ \|  _ \/ ___|
# \___ \|  _| | |   |  _|| |     | || | | | |_) \___ \
#  ___) | |___| |___| |__| |___  | || |_| |  _ < ___) |
# |____/|_____|_____|_____\____| |_| \___/|_| \_\____/
#

def select_children(pred):
    def _select(nodes):
        if is_branch(nodes):
            return nfilter(pred, nodes.children)
        elif is_leaf(nodes):
            return NodeSet()
        elif is_nset(nodes):
            return map_union(select_children(pred), nodes)
        else:
            raise ValueError("Can't select children for non-node: %s of type %s",
                             nodes, type(nodes))
    return _select

select_all_children = select_children(lambda _: True)


def select_descendants(pred):
    selector = select_children(pred)
    def _select(nodes):
        res = NodeSet()
        nodes = nodes.as_node_set()

        while nodes:
            current = nodes[0]
            nodes = nodes[1:]
            res.append(current)
            nodes = selector(current) + nodes

        return res
    return _select

select_all_descendants = select_descendants(lambda _: True)


@make_mapper
def select_text(node):
    if is_leaf(node):
        return NodeSet(node.val)
    return select_text(node.children)
