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
python main.py examples/hello_world.mylang
```

### Interactive Console

```bash
python main.py
```

### Using as Python Module

```bash
python -m mylang examples/hello_world.mylang
```

### Installation

```bash
pip install -e .
mylang examples/hello_world.mylang
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

### Hello World

```mylang
print("Hello, World!");
```

### Simple Calculator

```mylang
int a = 10;
int b = 3;
print("a + b =", a + b);
```

See the `examples/` directory for more comprehensive examples:

- `examples/hello_world.mylang` - Basic hello world
- `examples/calculator.mylang` - Arithmetic operations
- `examples/fibonacci.mylang` - Recursive functions
- `examples/comprehensive_test.mylang` - Full language features

## Extending the Language

The language is designed to be easily extensible. See `examples/extension_demo.py` for examples of adding new built-in functions like `len()`, `max()`, `min()`, and `abs()`.

## Architecture

The language implementation consists of:

- **src/mylang/lexer.py**: Tokenization
- **src/mylang/parser.py**: Syntax analysis and AST generation  
- **src/mylang/ast.py**: Abstract Syntax Tree node definitions
- **src/mylang/evaluator.py**: AST evaluation with proper scoping
- **src/mylang/error.py**: Comprehensive error handling system
- **src/mylang/builtins.py**: Extensible built-in function system
- **src/mylang/tokens.py**: Token type definitions

## File Structure

```text
mylang/
├── main.py                           # Main interpreter entry point
├── setup.py                          # Python package setup
├── README.md                         # This file
├── src/
│   └── mylang/                       # Core language package
│       ├── __init__.py              # Package initialization
│       ├── __main__.py              # Module entry point  
│       ├── lexer.py                 # Tokenizer
│       ├── parser.py                # Parser
│       ├── ast.py                   # AST node classes
│       ├── evaluator.py             # Evaluator with scoping
│       ├── error.py                 # Error handling
│       ├── builtins.py              # Built-in functions
│       └── tokens.py                # Token configuration
├── examples/                         # Example programs
│   ├── hello_world.mylang           # Basic hello world
│   ├── calculator.mylang            # Arithmetic demo
│   ├── fibonacci.mylang             # Recursive functions
│   ├── comprehensive_test.mylang    # Full feature test
│   └── extension_demo.py            # Extensibility demo
├── tests/                           # Unit tests
│   └── test_mylang.py              # Test suite
└── docs/                           # Documentation
    ├── language_spec.md            # Language specification
    └── REFACTORING_SUMMARY.md     # Implementation details
```

## Development

The language uses a clean, modular architecture that makes it easy to:

- Add new language features
- Extend with new built-in functions
- Implement optimizations
- Add better error reporting
- Build development tools

For implementation details, see `REFACTORING_SUMMARY.md`.
