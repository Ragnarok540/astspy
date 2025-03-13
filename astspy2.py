import ast
from csv import writer
import os
from os.path import join, splitext, isdir
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
        res.append(type(dictionary[key]).__name__[:-3])
        res.append(dictionary[key].name)
        res.append(str(dictionary[key].end_lineno - key + 1))
        doc_str = ast.get_docstring(dictionary[key])
        res.append("Yes" if doc_str else "No")

        result.append(res)

    return result


# names = file_names('./test_folder_0')
if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        print("[ERROR] no directory path provided")
        sys.exit()

    if not isdir(path):
        print("[ERROR] path provided is not a directory")
        sys.exit()

    names = file_names(path)
    result = [['PATH',
               'LINES',
               'LOCATION',
               'TYPE',
               'NAME',
               'SIZE',
               'DOCSTRING']]

    for name in names:
        res = analyze_file(name)
        result.extend(res)

    with open('output.csv', mode='w', newline='') as csv_file:
        csv_writer = writer(csv_file)

        for row in result:
            csv_writer.writerow(row)
