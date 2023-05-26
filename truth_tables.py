"""
Logical Truth Table Module
"""
from collections.abc import Iterator
from itertools import product
from typing import Type, TypeVar
# LOCAL #
from logical.syntax import *

__all__ = ['is_contingency', 'is_contradiction', 'is_tautology', 'result', 'truth_values']

_T = TypeVar('_T')


def truth_values(n: int, /, *, cast: Type[_T] = TruthVar) -> Iterator[tuple[_T, ...]]:
    """
    :returns: truth values in binary order (from all False to all True)

    >>> for row in truth_values(3): print(*row)
    F F F
    F F T
    F T F
    F T T
    T F F
    T F T
    T T F
    T T T
    """
    return product([cast(0), cast(1)], repeat=n)


def result(proposition: Proposition, cast: Type[_T] = TruthVar) -> list[TruthVar]:
    """
    :returns: truth table result in binary order (from all False to all True)
    """
    n = proposition.__code__.co_argcount
    return [proposition(*vars_) for vars_ in truth_values(n, cast=cast)]


def steps(proposition: Proposition) -> list[TruthVar]:
    """
    :returns: truth table steps in binary order (from all False to all True)
    """
    # n = len(signature(proposition).parameters)
    raise NotImplementedError


def is_tautology(proposition: Proposition) -> bool:
    return bool(result(proposition) == T)


def is_contradiction(proposition: Proposition) -> bool:
    return bool(result(proposition) == F)


def is_contingency(proposition: Proposition) -> bool:
    return not (is_tautology(proposition) or is_contradiction(proposition))

# TODO: https://www.gatevidyalay.com/tag/satisfiability-and-tautology/


def doctest_operators() -> None:
    """
    >>> # NEGATION
    >>> result(lambda p: p)
    [0, 1]
    >>> result(lambda p: ~p)
    [1, 0]
    >>> # CONJUNCTION
    >>> result(lambda p, q: p & q)
    [0, 0, 0, 1]
    >>> # DISJUNCTION
    >>> result(lambda p, q: p | q)
    [0, 1, 1, 1]
    >>> # IMPLICATION
    >>> result(lambda p, q: p >> q)
    [1, 1, 0, 1]
    >>> # CONSEQUENCE
    >>> result(lambda p, q: p << q)
    [1, 0, 1, 1]
    >>> # EQUIVALENCE
    >>> result(lambda p, q: p == q)
    [1, 0, 0, 1]
    >>> # INEQUIVALENCE
    >>> result(lambda p, q: p != q)
    [0, 1, 1, 0]
    """


def doctest_tf_laws() -> None:
    """
    >>> F
    0
    >>> T
    1

    >>> result(lambda p: p & T) == result(lambda p: p)
    1
    >>> result(lambda p: p & F) == F
    1
    >>> result(lambda p: p & ~p) == F
    1

    >>> result(lambda p: p | T) == T
    1
    >>> result(lambda p: p | F) == result(lambda p: p)
    True
    >>> result(lambda p: p | ~p) == T
    1

    >>> result(lambda p: p >> T) == T
    1
    >>> result(lambda p: F >> p) == T
    1
    >>> result(lambda p: p >> p) == T
    1

    >>> result(lambda p: p == T) == result(lambda p: p)
    True
    >>> result(lambda p: p == F) == result(lambda p: ~p)
    True
    >>> result(lambda p: p == p) == T
    1
    """


def doctest_propositions() -> None:
    """
    >>> result(lambda p, q, r: (p & (r | (~r))) >> ((q & q) | (~q)))
    [1, 1, 1, 1, 1, 1, 1, 1]
    >>> result(lambda p, q, r: ((p == r) & (r == q)) >> (p == q))
    [1, 1, 1, 1, 1, 1, 1, 1]
    >>> result(lambda p, q, s, t: ~((s >> t) & (p | q)) == (~(s >> t) | ~(p | q)))
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    >>> result(lambda p, q, r: r >> (p | q))
    [1, 0, 1, 1, 1, 1, 1, 1]
    >>> result(lambda p, q, r: (p & (r | ~r)) >> ((q & q) | ~q))
    [1, 1, 1, 1, 1, 1, 1, 1]
    """


def doctest_tautologies_and_consequences() -> None:
    """
    >>> is_tautology(lambda p, q, r: ((p & q) >> r) == ((p >> r) | (q >> r)))
    True
    >>> is_tautology(lambda p, q, r: ((p | q) >> r) >> ((p & r) >> r))
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    print(is_contradiction(lambda p, q: ((~(p & q) | q) >> (~p & p))))
