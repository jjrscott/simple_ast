
# `$ python3 simple_ast.py --help` for more information

import argparse
import os
import json
import re

def main():
    parser = argparse.ArgumentParser(description='Generate a simple abstract syntax tree from the given files', epilog="""

Parsing rules

This parser uses three values:
  bounds A dictionary of start and end tokens. If the program finds a start
         token it will push a new array on the stack and continue. When it
         finds the corresponding end token the program will pop the array off
         the stack and continue.
  extra  An array of tokens that don't push or pop when found (unless they're
         in the bounds).
  strip  An array of tokens that will be removed from the output.

Example rules:

{
  "bounds": { "(": ")" },
  "extra": [ "-", "+", "*", "/", "%" ],
  "strip": [ "\n", " " ]
}

    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='+', help='Files to be parsed')
    parser.add_argument('--output', default='-', help='Location to save the AST')
    parser.add_argument('--rules', help='A JSON file containing the parsing rules')
    args = parser.parse_args()

    rules = {}
    if args.rules:
        with open(args.rules, 'r') as f:
            rules = json.load(f)

    if 'bounds' not in rules:
        rules['bounds'] = {}
    if 'extra' not in rules:
        rules['extra'] = ['\n']
    if 'strip' not in rules:
        rules['strip'] = []

    if args.rules:
        with open(args.rules, "w") as file:
            file.write(json.dumps(rules, sort_keys=True, indent=2))

    ast = {}

    for input_path in args.input:
        with open(input_path, 'r') as file:
            text = file.read()
            ast[input_path] = generate_ast(text, bounds=rules['bounds'], extra=rules['extra']+rules['strip'], strip=rules['strip'])

    if len(ast) == 1:
        ast = list(ast.values())[0]

    outputContent = json.dumps(ast, sort_keys=True, indent=2)

    if args.output != '-':
        with open(args.output, "w") as file:
            file.write(outputContent)
    else:
        print(outputContent)


def generate_ast(text, bounds={}, extra=['\n'], strip=['\n']):
    boundingTokenRegex = '|'.join(map(lambda s: "("+re.escape(s)+")", sorted(list(bounds.keys()) + list(bounds.values()) + extra,reverse=True)))
    tokens = re.compile(boundingTokenRegex).split(text)
    stack = [[]]

    for token in tokens:
        if token is None or len(token) == 0:
            continue

        if token in bounds:
            frame = []
            stack[-1].append(frame)
            stack.append(frame)

        if token not in strip:
            stack[-1].append(token)

        if len(stack) > 1 and isinstance(stack[-1][0], str) and stack[-1][0] in bounds and token == bounds[stack[-1][0]]:
            stack.pop()

    return stack[0]

if __name__ == "__main__":
    main()
