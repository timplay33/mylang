"""
MyLang Programming Language
A simple, strongly-typed programming language with modern architecture.
"""

__version__ = "1.0.0"
__author__ = "MyLang Team"

# Import main components for easy access
from .lexer import tokenize
from .parser import Parser
from .evaluator import Environment, Evaluator
from .error import LanguageError, SyntaxError, TypeError, RuntimeError
from .ast import *
from .builtins import BuiltinRegistry

__all__ = [
    'tokenize',
    'Parser',
    'Environment',
    'Evaluator',
    'LanguageError',
    'SyntaxError',
    'TypeError',
    'RuntimeError',
    'BuiltinRegistry'
]
