import ast
import csv
import os
import os.path
import sys


def file_names(directory: str) -> list[str]:
    result = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            _, ext = os.path.splitext(name)

            if ext == '.py':
                result.append(os.path.join(root, name))

    return result


def analyze_file(path: str) -> list[list[str]]:
    file = open(path)
    code = file.read()
    lines = sum(1 for _ in open(path))
    tree = ast.parse(code)
    result = []
    dictionary = {}

    for node in ast.walk(tree):
        cl = isinstance(node, ast.ClassDef)
        fn = isinstance(node, ast.FunctionDef)
        afn = isinstance(node, ast.AsyncFunctionDef)

        if any([cl, fn, afn]):
            dictionary[node.lineno] = node

    for key in sorted(dictionary):
        res = []
        res.append(path)
        res.append(str(lines))
        res.append(str(key))
        res.append(type(dictionary[key]).__name__[:-3])
        res.append(dictionary[key].name)
        if isinstance(dictionary[key], ast.ClassDef):
            res.append('')
        else:
            res.append(str([arg.arg for arg in dictionary[key].args.args]))
        res.append(str([Name.id for Name in dictionary[key].decorator_list]))
        if isinstance(dictionary[key], ast.ClassDef):
            res.append(str([Name.id for Name in dictionary[key].bases]))
        else:
            res.append('')
        res.append(str(dictionary[key].end_lineno - key + 1))
        doc = ast.get_docstring(dictionary[key])
        res.append("Yes" if doc else "No")

        result.append(res)

    return result


if __name__ == '__main__':
    try:
        path = sys.argv[1]  # './test_folder_0'
    except IndexError:
        print("[ERROR] no directory path provided")
        sys.exit()

    if not os.path.isdir(path):
        print("[ERROR] path provided is not a directory")
        sys.exit()

    try:
        write_csv = sys.argv[2]  # '--write-csv'
        if write_csv == '--write-csv':
            stdout = False
        else:
            stdout = True
    except IndexError:
        stdout = True

    names = file_names(path)
    result = [['PATH',
               'LINES',
               'LOCATION',
               'TYPE',
               'NAME',
               'ARGS',
               'DECORATORS',
               'BASES',
               'SIZE',
               'DOCSTRING']]

    for name in names:
        res = analyze_file(name)
        result.extend(res)

    if stdout:
        output = sys.stdout
    else:
        output = open('output.csv', mode='w', newline='')

    with output as csv_file:
        csv_writer = csv.writer(csv_file)

        for row in result:
            csv_writer.writerow(row)
