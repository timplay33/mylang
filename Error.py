from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceLocation:
    line: int
    column: int
    filename: Optional[str] = None

    def __str__(self):
        if self.filename:
            return f"{self.filename}:{self.line}:{self.column}"
        return f"{self.line}:{self.column}"


class LanguageError(Exception):
    """Base class for all language errors"""

    def __init__(self, message: str, location: Optional[SourceLocation] = None):
        self.message = message
        self.location = location
        super().__init__(self.format_error())

    def format_error(self) -> str:
        if self.location:
            return f"Error at {self.location}: {self.message}"
        return f"Error: {self.message}"


class SyntaxError(LanguageError):
    """Syntax errors during parsing"""
    pass


class TypeError(LanguageError):
    """Type-related errors"""
    pass


class RuntimeError(LanguageError):
    """Runtime errors during execution"""
    pass


class EvaluationError(RuntimeError):
    """Base class for evaluation errors"""
    pass


class TypeMismatchError(EvaluationError):
    """Raised when types don't match in operations"""
    pass


class UndefinedVariableError(EvaluationError):
    """Raised when accessing undefined variables"""
    pass


class UndefinedFunctionError(EvaluationError):
    """Raised when calling undefined functions"""
    pass
