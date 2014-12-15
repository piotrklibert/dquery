from operator import attrgetter
from funcy import curry, all, compose, isa


class Node(object):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def named(self, name):
        try:
            if isinstance(name, basestring) and isinstance(self.name, basestring):
                return self.name.lower() == name.lower()
            else:
                return str(self.name) == str(name)
        except Exception:
            return False

    def as_node_set(self):
        return NodeSet(self)




class Branch(Node):
    def __init__(self, name, children):
        self.name = name
        self.val = NodeSet(*children)

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


class NodeSet(list):
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


def is_branch(obj):
    return isinstance(obj, Node) and not isinstance(obj, Leaf)

def is_leaf(obj):
    return isinstance(obj, Leaf)

def is_single(obj):
    return is_leaf(obj) or not isinstance(obj, (Node, NodeSet, list))



def nodify(name, data):
    _nodify = lambda (name, data): nodify(name, data)
    if isinstance(data, list):
        return Branch(name, NodeSet(*map(_nodify, enumerate(data))))
    elif isinstance(data, dict):
        return Branch(name, NodeSet(*map(_nodify, data.iteritems())))
    else:
        return Leaf(name, data)



def map_union(proc, lst):
    res = NodeSet()
    for node in lst:
        res.append_or_extend(proc(node))
    return res



def nfilter(pred, nodes):
    return NodeSet(*filter(pred, nodes.as_node_set()))


make_filter = curry(nfilter)

def make_mapper(func):
    def _mapper(nodes):
        return map_union(func, nodes.as_node_set())
    return _mapper


def select_children(pred):
    def _select(nodes):
        if is_branch(nodes):
            return nfilter(pred, nodes.children)

        if is_leaf(nodes):
            return NodeSet()

        return map_union(select_children(pred), nodes)
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


def compose_selectors(*selectors):
    def _composed(nodes):
        res = nodes
        for selector in selectors:
            res = selector(res)
        return res

    return _composed



@make_mapper
def select_text(node):
    if is_leaf(node):
        return NodeSet(node.val)
    return select_text(node.children)
