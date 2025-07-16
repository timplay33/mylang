from typing import Any, List, Callable
from abc import ABC, abstractmethod
from .error import RuntimeError


class BuiltinFunction(ABC):
    """Base class for built-in functions"""

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def call(self, args: List[Any]) -> Any:
        pass

    @abstractmethod
    def validate_args(self, args: List[Any]) -> bool:
        pass


class PrintFunction(BuiltinFunction):
    def name(self) -> str:
        return 'print'

    def call(self, args: List[Any]) -> Any:
        print(*args)
        return None

    def validate_args(self, args: List[Any]) -> bool:
        return True  # Print accepts any number of arguments


class TypeConversionFunction(BuiltinFunction):
    def __init__(self, target_type: str, converter: Callable):
        self._name = f'to{target_type.capitalize()}'
        self.converter = converter
        self.target_type = target_type

    def name(self) -> str:
        return self._name

    def call(self, args: List[Any]) -> Any:
        if len(args) != 1:
            raise RuntimeError(f"{self.name()} expects exactly 1 argument")
        try:
            return self.converter(args[0])
        except (ValueError, TypeError) as e:
            raise RuntimeError(
                f"Cannot convert {args[0]} to {self.target_type}: {e}")

    def validate_args(self, args: List[Any]) -> bool:
        return len(args) == 1


class BuiltinRegistry:
    """Registry for built-in functions"""

    def __init__(self):
        self.functions: dict[str, BuiltinFunction] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register default built-in functions"""
        builtins = [
            PrintFunction(),
            TypeConversionFunction('int', int),
            TypeConversionFunction('float', float),
            TypeConversionFunction('string', str),
        ]

        for builtin in builtins:
            self.register(builtin)

    def register(self, function: BuiltinFunction):
        """Register a new built-in function"""
        self.functions[function.name()] = function

    def call(self, name: str, args: List[Any]) -> Any:
        """Call a built-in function"""
        if name not in self.functions:
            raise RuntimeError(f"Unknown built-in function: {name}")

        function = self.functions[name]
        if not function.validate_args(args):
            raise RuntimeError(f"Invalid arguments for {name}")

        return function.call(args)

    def has_function(self, name: str) -> bool:
        """Check if a function is registered"""
        return name in self.functions
