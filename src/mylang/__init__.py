"""
MyLang Programming Language
A simple, strongly-typed programming language with modern architecture.
"""

__version__ = "1.0.0"
__author__ = "Tim Heidler"

# Import main components for easy access
from .lexer import tokenize
from .parser import Parser
from .evaluator import Environment, Evaluator
from .error import LanguageError, SyntaxError, TypeError, RuntimeError
from .builtins import BuiltinRegistry
from .tokens import TokenType

__all__ = [
    'tokenize',
    'Parser',
    'Environment',
    'Evaluator',
    'LanguageError',
    'SyntaxError',
    'TypeError',
    'RuntimeError',
    'BuiltinRegistry',
    'TokenType'
]
