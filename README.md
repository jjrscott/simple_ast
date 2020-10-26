Simple AST takes a simple set of rules and produces a simple abstract syntax tree.


## Usage

```shell
python3 simple_ast.py --rules rules/calulator.json examples/calculator.txt
```

### Parsing rules

This parser uses three values:
- bounds A dictionary of start and end tokens. If the program finds a start token it will push a new array on the stack and continue. When it finds the corresponding end token the program will pop the array off the stack and continue.
- extra  An array of tokens that don't push or pop when found (unless they're in the bounds).
- strip  An array of tokens that will be removed from the output.

#### Example

##### Input
```
6 * (4 + 3)
```

##### Rules
```json
{
  "bounds": { "(": ")" },
  "extra": [ "-", "+", "*", "/", "%" ],
  "strip": [ "\n", " " ]
}
```

##### AST

```JSON
[
  "6",
  "*",
  [
    "(",
    "7",
    "+",
    "3",
    ")"
  ]
]
```
