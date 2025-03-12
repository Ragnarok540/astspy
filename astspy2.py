import ast
import os
from os.path import join, splitext
import sys


def file_names(directory: str) -> list[str]:
    result = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            _, ext = splitext(name)

            if ext == '.py':
                result.append(join(root, name))

    return result


def analyze_file(path: str) -> list[list[str]]:
    file = open(path)
    code = file.read()
    size = sum(1 for _ in open(path))
    tree = ast.parse(code)
    result = []
    dictionary = {}

    for node in ast.walk(tree):
        cl = isinstance(node, ast.ClassDef)
        fn = isinstance(node, ast.FunctionDef)
        afn = isinstance(node, ast.AsyncFunctionDef)

        if cl or fn or afn:
            dictionary[node.lineno] = node

    for key in sorted(dictionary):
        res = []
        res.append(path)
        res.append(str(size))
        res.append(str(key))
        res.append(dictionary[key].name)
        res.append(str(dictionary[key].end_lineno - key + 1))
        doc_str = ast.get_docstring(dictionary[key])
        res.append("YES" if doc_str else "NO")

        result.append(res)

    return result


if __name__ == '__main__':
    path = sys.argv[1]
    names = file_names('./test_folder_0')
    print(analyze_file(names[0]))
