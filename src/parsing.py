import sexpdata


def normalise_tree(tree):

    def _normalise_tree(tree, wrap=True):
        from tree import Tree

        if type(tree) is list and len(tree) > 1:
            fun, *params = tree
            assert len(params)
            result = [fun.value(), *(map(_normalise_tree, params))]
        elif type(tree) is list:
            result = float(tree[0])
        else:
            result = tree

        if wrap:
            result = Tree(result)
        return result

    return _normalise_tree(tree, wrap=False)


def parse(expression):
    return normalise_tree(sexpdata.loads(expression))