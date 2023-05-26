"""
Structure
"""
import operator

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import cached_property, total_ordering
from itertools import product
from math import gcd, isqrt, lcm
from typing import TypeVar
# LOCAL
from logical.gates.binary import AND, OR
from logical.gates.unary import NOT

__all__ = [
    'B',                                                         # Structure
    'D',                                                         # Structure Factory
    'GF2', 'GF3', 'GF5', 'GF7', 'GF11', 'GF13', 'GF17', 'GF19',  # Galois Fields
    'Element',
    'Structure',
    'Field'
]

_T = TypeVar('_T')
Element = TypeVar('Element')


def find_additive_identity(elements: Iterable[_T]) -> _T | None:
    return next((x for x in elements if all(x + y == y for y in elements)), None)


def find_multiplicative_identity(elements: Iterable[_T]) -> _T | None:
    return next((x for x in elements if all(x * y == y for y in elements)), None)


@dataclass
class Structure(Iterable):
    """
    Class for Minimal Boole-Algebra Structure
    """

    name: str
    set: set[int]
    add: Callable[[int, int], int]
    mul: Callable[[int, int], int]
    inv: Callable[[int], int]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' \
               f'name={self.name!r}, ' \
               f'set={self.set}, ' \
               f'add={self.add.__name__}, ' \
               f'mul={self.mul.__name__}, ' \
               f'inv={self.inv.__name__})'

    def __post_init__(self) -> None:
        self._elements = {el: self._generate_element(el) for el in self.set}
        id_add = find_additive_identity(self.elements)
        if id_add is not None: self.identity_add: Element = id_add
        id_mul = find_multiplicative_identity(self.elements)
        if id_mul is not None: self.identity_mul: Element = id_mul

    def __getitem__(self, identity: int) -> Element:
        if identity == 0:
            return getattr(self, 'identity_add', float('nan'))
        if identity == 1:
            return getattr(self, 'identity_mul', float('nan'))
        raise ValueError(f'invalid identity: {identity} not in {{0, 1}} ')

    @cached_property
    def elements(self):
        return set(self._elements.values())

    def __str__(self) -> str:
        return self.name

    def __iter__(self) -> iter:
        return iter(self._elements)

    def __call__(self, value: int) -> Element:
        if value in self._elements: return self._elements[value]
        raise ValueError(f'value: {value} not in {self.set}')

    # noinspection PyShadowingNames
    def _generate_element(self, value: int) -> Element:
        instance = self

        @total_ordering
        class Element:
            def __init__(self, __value: int) -> None:
                self.value = __value

            def __repr__(self) -> str:
                return f'{instance.name}({self.value})'

            def __str__(self) -> str:
                return str(self.value)

            def __index__(self) -> int:
                return self.value

            def __hash__(self) -> int:
                return self.value

            def __bool__(self) -> bool:
                return bool(self.value)

            def __eq__(self, other) -> bool:
                return self.value == other.value

            def __lt__(self, other) -> bool:
                return self.value < other.value

            def __add__(self, other) -> 'Element':
                return Element(instance.add(self.value, other.value))

            def __mul__(self, other) -> 'Element':
                return Element(instance.mul(self.value, other.value))

            def __neg__(self) -> 'Element':
                return Element(instance.inv(self.value))

        if value in self.set:
            return Element(value)
        raise ValueError(f'invalid value: {value} not in {self.set}')

    def operands(self, n: int) -> Iterable[Element]:
        return product(sorted(self.elements), repeat=n)

    def bind(self, formula: Callable) -> Callable[..., ...]:
        """ Binds Formula to Structure """
        return lambda *args: formula(*map(self.__call__, args))


B = Structure('B', {0, 1}, OR, AND, NOT)  # Boolean Structure


class D:
    """
    DIV Factory Class
    """

    def __new__(cls, n: int) -> Structure:
        def floordiv(divisor: int) -> int:
            return n // divisor

        divisors = {i for k in range(1, isqrt(n) + 1) if not n % k for i in {k, n // k}}
        return Structure(f'D{n}', divisors, lcm, gcd, floordiv)


@dataclass
class Field(Iterable):
    """
    """

    name: str
    ord: int  # order
    add: Callable[[int, int], int]  # addition
    mul: Callable[[int, int], int]  # multiplication

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' \
               f'name={self.name!r}, ' \
               f'ord={self.ord}, ' \
               f'add={self.add.__name__}, ' \
               f'mul={self.mul.__name__})'

    def __post_init__(self) -> None:
        self._elements = {el: self._generate_element(el) for el in range(self.ord)}
        id_add = find_additive_identity(self.elements)
        if id_add is not None: self.identity_add: Element = id_add
        id_mul = find_multiplicative_identity(self.elements)
        if id_mul is not None: self.identity_mul: Element = id_mul

    def __getitem__(self, identity: int) -> Element:
        if identity == 0:
            return getattr(self, 'identity_add', float('nan'))
        if identity == 1:
            return getattr(self, 'identity_mul', float('nan'))
        raise ValueError(f'invalid identity: {identity} not in {{0, 1}} ')

    @property
    def elements(self) -> set[Element]:
        return set(self._elements.values())

    def add_inv(self, other: Element) -> Element:  # additive inverse -> -a
        if other == self[0]: return other
        return next((el for el in self.elements if other + el == self[0]), self[0])

    def pow(self, base: Element, exp: int) -> Element:
        if exp < 0: return self.mul_inv(self.pow(base, -exp))
        if self.ord in {0, 1}: return self[0]
        if exp == 0: return self[1]
        if base in {self[0], self[1]}: return base
        res = self[1]
        while exp:
            if exp & 1: res *= base
            exp >>= 1
            base *= base
        return res

    def mul_inv(self, other: Element) -> Element:  # multiplicative inverse -> a ** -1
        if other == self[0]: return float('nan')
        if other == self[1]: return other
        return next((el for el in self.elements if other * el == self[1]), self[1])

    def __str__(self) -> str:
        return self.name

    def __iter__(self):
        return iter(self._elements)

    def __call__(self, value: int) -> Element:
        return self._elements[value % self.ord]

    # noinspection PyShadowingNames
    def _generate_element(self, value: int) -> Element:
        instance = self

        @total_ordering
        class Element:
            def __init__(self, __value: int) -> None:
                self.value = __value % instance.ord

            def __repr__(self) -> str:
                return f'{instance.name}({self.value})'

            def __str__(self) -> str:
                return str(self.value)

            def __index__(self) -> int:
                return self.value

            def __hash__(self) -> int:
                return self.value

            def __bool__(self) -> bool:
                return bool(self.value)

            def __eq__(self, other) -> bool:
                return self.value == other.value

            def __lt__(self, other) -> bool:
                return self.value < other.value

            def __add__(self, other) -> 'Element':
                return Element(instance.add(self.value, other.value))

            def __mul__(self, other) -> 'Element':
                return Element(instance.mul(self.value, other.value))

            def __pow__(self, other) -> 'Element':
                return instance.pow(self, other)

            def __neg__(self) -> 'Element':
                return instance.add_inv(self)

        return Element(value)

    def operands(self, n: int) -> Iterable[Element]:
        return product(sorted(self.elements), repeat=n)

    def bind(self, function: Callable) -> Callable[..., ...]:
        """ Binds Function to Field """
        return lambda *args: function(*map(self.__call__, args))


GF2 = Field('GF2', 2, operator.add, operator.mul)
GF3 = Field('GF3', 3, operator.add, operator.mul)
GF5 = Field('GF5', 5, operator.add, operator.mul)
GF7 = Field('GF7', 7, operator.add, operator.mul)
GF11 = Field('GF11', 11, operator.add, operator.mul)
GF13 = Field('GF13', 13, operator.add, operator.mul)
GF17 = Field('GF17', 17, operator.add, operator.mul)
GF19 = Field('GF19', 19, operator.add, operator.mul)

if __name__ == '__main__':
    import doctest

    doctest.testmod()
