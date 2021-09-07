"""Functions related to typing."""
from enum import Enum, EnumMeta
from typing import Any, Callable, TypeVar, get_type_hints

__all__ = ["enum_name_str", "implements", "parsable"]

_F = TypeVar("_F", bound=Callable[..., Any])


class implements:  # pylint: disable=invalid-name
    """Mark a function as implementing an interface."""

    def __init__(self, interface: type):
        """Instantiate the decorator.

        Args:
            interface: the interface that is implemented
        """
        self.interface = interface

    def __call__(self, func: _F) -> _F:
        """Take a function and return it unchanged."""
        super_method = getattr(self.interface, func.__name__, None)
        assert super_method is not None, f"'{func.__name__}' does not exist in {self.interface}"
        return func


def parsable(func: _F) -> _F:
    """Mark an object's __init__ as parsable by Configen, so only pre-3.9 type annotations should be used."""
    assert func.__name__ == "__init__", "@parsable can only be used to decorate __init__."
    try:
        get_type_hints(func)
    except TypeError:
        raise ValueError(
            "the type annotations of this function are not automatically parseable."
        ) from None
    return func


E = TypeVar("E", bound=EnumMeta)


def enum_name_str(enum_class: E) -> E:
    """Patch the __str__ method of an enum so that it returns the name."""

    def __str__(self: Enum) -> str:
        return self.name

    enum_class.__str__ = __str__  # type: ignore
    return enum_class
