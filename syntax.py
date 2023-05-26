"""
Logical Syntax Module
"""
from collections.abc import Callable, Iterable

__all__ = ['Proposition', 'F', 'T', 'TruthVar', 'TruthVarException']


class TruthVarException(Exception):
    pass


class TruthVar(int):
    def __new__(cls, value: int) -> 'TruthVar':
        return super().__new__(cls, bool(value))

    def __str__(self) -> str:
        return 'T' if self.real else 'F'

    def __and__(self, other: int) -> 'TruthVar':
        return TruthVar(self.real and other.real)

    def __eq__(self, other: int | Iterable[int]) -> 'TruthVar':
        if isinstance(other, TruthVar):
            return TruthVar(self.real == other.real)
        if isinstance(other, Iterable):
            return TruthVar(all(map(self.real.__eq__, other)))
        return NotImplemented

    def __rshift__(self, other: int) -> 'TruthVar':
        return TruthVar(not self.real or other.real)

    def __lshift__(self, other: int) -> 'TruthVar':
        return TruthVar(self.real or not other.real)

    def __invert__(self) -> 'TruthVar':
        return TruthVar(not self.real)

    def __or__(self, other: int) -> 'TruthVar':
        return TruthVar(self.real or other.real)

    def __ne__(self, other: int | Iterable[int]) -> 'TruthVar':
        if isinstance(other, TruthVar):
            return TruthVar(self.real != other.real)
        if isinstance(other, Iterable):
            return TruthVar(all(map(self.real.__ne__, other)))
        return NotImplemented

    def __hash__(self) -> int:
        return self.real

    __add__ = __or__
    __mul__ = __and__
    __neg__ = __invert__


Proposition = Callable[..., bool | int | TruthVar]

F = TruthVar(0)
T = TruthVar(1)
