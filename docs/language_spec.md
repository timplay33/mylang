# MyLang Language Specification

## Syntax Reference

### Variables

```mylang
type_name variable_name = initial_value;
```

Supported types:

- `int`: Integer numbers (e.g., 42, -10)
- `float`: Floating-point numbers (e.g., 3.14, -2.5)
- `string`: Text strings (e.g., "Hello World")
- `bool`: Boolean values (`true` or `false`)

### Functions

```mylang
func return_type function_name(type param1, type param2) {
    // function body
    return value;
}
```

### Control Structures

#### If Statement

```mylang
if (condition) {
    // statements
} else {
    // statements
}
```

#### While Loop

```mylang
while (condition) {
    // statements
}
```

### Operators

#### Arithmetic

- `+`: Addition
- `-`: Subtraction  
- `*`: Multiplication
- `/`: Division

#### Comparison

- `==`: Equal
- `!=`: Not equal
- `<`: Less than
- `>`: Greater than
- `<=`: Less than or equal
- `>=`: Greater than or equal

#### Logical

- `&&`: Logical AND
- `||`: Logical OR
- `!`: Logical NOT

#### Assignment

- `=`: Basic assignment
- `++`: Increment (postfix)
- `--`: Decrement (postfix)

### Built-in Functions

- `print(args...)`: Print arguments to console
- `toInt(value)`: Convert to integer
- `toFloat(value)`: Convert to float
- `toString(value)`: Convert to string

### Comments

```mylang
// Single line comment

/* 
   Multi-line
   comment
*/
```

## Grammar (EBNF)

```ebnf
program = statement*

statement = declaration
          | assignment  
          | function_declaration
          | if_statement
          | while_statement
          | expression_statement
          | return_statement

declaration = type IDENTIFIER "=" expression ";"

assignment = IDENTIFIER "=" expression ";"

function_declaration = "func" type IDENTIFIER "(" parameter_list? ")" block

parameter_list = parameter ("," parameter)*
parameter = type IDENTIFIER

block = "{" statement* "}"

if_statement = "if" "(" expression ")" block ("else" block)?

while_statement = "while" "(" expression ")" block

expression_statement = expression ";"

return_statement = "return" expression? ";"

expression = logical_or

logical_or = logical_and ("||" logical_and)*

logical_and = equality ("&&" equality)*

equality = comparison (("==" | "!=") comparison)*

comparison = term (("<" | ">" | "<=" | ">=") term)*

term = factor (("+" | "-") factor)*

factor = unary (("*" | "/") unary)*

unary = ("!" | "-") unary | primary

primary = NUMBER | STRING | BOOLEAN | IDENTIFIER 
        | function_call | "(" expression ")"

function_call = IDENTIFIER "(" argument_list? ")"

argument_list = expression ("," expression)*
```
