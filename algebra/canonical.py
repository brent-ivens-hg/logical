"""
Canonical
"""
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from math import prod
from inspect import signature
# LOCAL #
from logical.algebra.functions import table
from logical.algebra.structure import *


@dataclass(frozen=True, slots=True)
class CanonicalForm:
    struct: Structure
    formula: Callable


@dataclass(frozen=True, slots=True)
class DNF(CanonicalForm):
    """  The Disjunctive Normal Form Of The Given Formula """

    def __iter__(self) -> Iterable[Element]:
        """ :returns: The Minimum Terms """
        n = len(signature(self.formula).parameters)
        for operands in self.struct.operands(n):
            if self.formula(*operands):
                yield operands

    def __str__(self) -> str:
        params = signature(self.formula).parameters
        return '+'.join(
            ''.join('%s%s' % (x, '' if op else '\u0304') for x, op in zip(params, operands)) for operands in self)

    def ascii(self) -> str:
        params = signature(self.formula).parameters
        return ' + '.join(
            '*'.join('%s%s' % ('' if op else '-', x) for x, op in zip(params, operands))
            for operands in self)

    def __call__(self) -> Element:
        return sum((prod((op for op in operands), start=self.struct.identity_mul)
                    for operands in self), start=self.struct.identity_add)


@dataclass(frozen=True, slots=True)
class CNF(CanonicalForm):
    """  The Conjunctive Normal Form Of The Given Formula """

    def __iter__(self) -> Iterable[Element]:
        """ :returns: The Maximum Terms """
        n = len(signature(self.formula).parameters)
        for operands in self.struct.operands(n):
            if not self.formula(*operands):
                yield tuple(-op for op in operands)

    def __str__(self) -> str:
        params = signature(self.formula).parameters
        return ''.join(
            '(%s)' % '+'.join('%s%s' % (x, '' if op else '\u0304') for x, op in zip(params, operands))
            for operands in self)

    def __call__(self) -> Element:
        return prod((sum((op for op in operands), start=self.struct.identity_add)
                     for operands in self), start=self.struct.identity_mul)

    def ascii(self) -> str:
        params = signature(self.formula).parameters
        return ' * '.join(
            '(%s)' % '+'.join('%s%s' % ('' if op else '-', x) for x, op in zip(params, operands))
            for operands in self)


def doctest_canonical_forms() -> None:
    """
    >>> f = lambda x, y, z: -(x + y + z)
    >>> table(B, formula=f)
    0  0  0 | 1
    0  0  1 | 0
    0  1  0 | 0
    0  1  1 | 0
    1  0  0 | 0
    1  0  1 | 0
    1  1  0 | 0
    1  1  1 | 0
    >>> dnf = DNF(B, f)
    >>> list(dnf)
    [(B(0), B(0), B(0))]
    >>> dnf.ascii()
    '-x*-y*-z'
    >>> print(dnf)
    x̄ȳz̄
    >>> dnf()
    B(0)
    >>> cnf = CNF(B, f)
    >>> cnf.ascii()
    '(x+y+-z) * (x+-y+z) * (x+-y+-z) * (-x+y+z) * (-x+y+-z) * (-x+-y+z) * (-x+-y+-z)'
    >>> list(cnf)
    [(B(1), B(1), B(0)), (B(1), B(0), B(1)), (B(1), B(0), B(0)), (B(0), B(1), B(1)), (B(0), B(1), B(0)), (B(0), B(0), B(1)), (B(0), B(0), B(0))]
    >>> print(cnf)
    (x+y+z̄)(x+ȳ+z)(x+ȳ+z̄)(x̄+y+z)(x̄+y+z̄)(x̄+ȳ+z)(x̄+ȳ+z̄)
    >>> cnf()
    B(0)

    >>> f = lambda x, y, z: (-x + y + -z) * -z * x
    >>> table(B, formula=f)
    0  0  0 | 0
    0  0  1 | 0
    0  1  0 | 0
    0  1  1 | 0
    1  0  0 | 1
    1  0  1 | 0
    1  1  0 | 1
    1  1  1 | 0
    >>> dnf = DNF(B, f)
    >>> print(dnf)
    xȳz̄+xyz̄
    >>> cnf = CNF(B, f)
    >>> print(cnf)
    (x+y+z)(x+y+z̄)(x+ȳ+z)(x+ȳ+z̄)(x̄+y+z̄)(x̄+ȳ+z̄)

    >>> f = lambda x, y, z: (x * (-y + z)) + -z
    >>> table(B, formula=f)
    0  0  0 | 1
    0  0  1 | 0
    0  1  0 | 1
    0  1  1 | 0
    1  0  0 | 1
    1  0  1 | 1
    1  1  0 | 1
    1  1  1 | 1
    >>> dnf = DNF(B, f)
    >>> print(dnf)
    x̄ȳz̄+x̄yz̄+xȳz̄+xȳz+xyz̄+xyz
    >>> cnf = CNF(B, f)
    >>> print(cnf)
    (x+y+z̄)(x+ȳ+z̄)

    >>> f = B.bind(lambda x, y: (x + -y) * (-x + -y))
    >>> f(1, 1).value
    0
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
