from __future__ import annotations
from typing import List, Union

import pytest

from kit.typing import parsable


def test_parsable():
    class Foo:
        @parsable
        def __init__(self):
            ...

    _ = Foo()


def test_parsable_valid():
    class Foo:
        @parsable
        def __init__(self, a: int, b: Union[int, float], c: List[str]):
            ...

    _ = Foo(a=1, b=1.2, c=["bar"])


def test_parsable_invalid_union():
    with pytest.raises(ValueError):

        class Foo:
            @parsable
            def __init__(self, a: int, b: int | float, c: List[str]):
                ...


def test_parsable_invalid_list():
    with pytest.raises(ValueError):

        class Foo:
            @parsable
            def __init__(self, a: int, b: Union[int, float], c: list[str]):
                ...
