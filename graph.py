import graphviz
import ast


def analyze_file(path: str):
    dot = graphviz.Digraph('function', comment='The Function')
    file = open(path)
    code = file.read()
    tree = ast.parse(code)
    nodes = {}
    sedon = {}

    for node in ast.walk(tree):
        fn = isinstance(node, ast.FunctionDef)

        if fn:
            nodes[node.lineno] = node
            sedon[node.name] = node.lineno
            dot.node(str(node.lineno), node.name)

    for key in sorted(nodes):
        for node in ast.walk(nodes[key]):
            ca = isinstance(node, ast.Call)

            if ca:
                try:
                    end = sedon[node.func.id]
                except KeyError:
                    print(f'function "{node.func.id}" in '
                          f'line {node.lineno} not found')
                    continue

                dot.edge(str(key), str(end))
                print([a.id for a in node.args])  # parameters

    print(dot.source)
    dot.format = 'png'  # svg
    dot.render(directory='doctest-output', view=True)


analyze_file('test_graph.py')
