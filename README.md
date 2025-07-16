# MyLang Programming Language

A simple, strongly-typed programming language with modern architecture and extensible design.

## Features

- **Strong Type System**: Integer, float, string, and boolean types with automatic type checking
- **Functions**: User-defined functions with parameters and return values
- **Control Flow**: if/else conditionals and while loops
- **Built-in Functions**: print, type conversion functions (toInt, toFloat, toString)
- **Extensible**: Easy to add new built-in functions
- **Modern Architecture**: Clean AST-based design with proper error handling

## Usage

### Running a MyLang Program

```bash
python main.py program.mylang
```

### Interactive Console

```bash
python main.py
```

## Language Syntax

### Variables

```mylang
int x = 10;
float pi = 3.14;
string message = "Hello World";
bool flag = true;
```

### Functions

```mylang
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

### Control Flow

```mylang
// Conditionals
if (x > 0) {
    print("Positive");
} else {
    print("Not positive");
}

// Loops
int i = 0;
while (i < 5) {
    print("Count:", i);
    i++;
}
```

### Built-in Functions

```mylang
print("Hello", "World");           // Output: Hello World
int num = toInt("42");             // Convert string to int
float f = toFloat(42);             // Convert to float
string s = toString(123);          // Convert to string
```

## Examples

See `test.mylang` for a comprehensive example program demonstrating all language features.

## Extending the Language

The language is designed to be easily extensible. See `extension_example.py` for examples of adding new built-in functions like `len()`, `max()`, `min()`, and `abs()`.

## Architecture

The language implementation consists of:

- **Lexer.py**: Tokenization
- **Parser.py**: Syntax analysis and AST generation
- **AST.py**: Abstract Syntax Tree node definitions
- **Evaluator.py**: AST evaluation with proper scoping
- **Error.py**: Comprehensive error handling system
- **Builtins.py**: Extensible built-in function system
- **TokenConfig.py**: Token type definitions

## File Structure

```
mylang/
├── main.py              # Main interpreter entry point
├── Lexer.py            # Tokenizer
├── Parser.py           # Parser
├── AST.py              # AST node classes
├── Evaluator.py        # Evaluator with scoping
├── Error.py            # Error handling
├── Builtins.py         # Built-in functions
├── TokenConfig.py      # Token configuration
├── test.mylang         # Example program
├── extension_example.py # Extensibility demo
└── README.md           # This file
```

## Development

The language uses a clean, modular architecture that makes it easy to:

- Add new language features
- Extend with new built-in functions
- Implement optimizations
- Add better error reporting
- Build development tools

For implementation details, see `REFACTORING_SUMMARY.md`.
