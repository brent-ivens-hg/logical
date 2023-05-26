"""
Boolean Algebra
"""
from collections.abc import Callable
from inspect import signature
# LOCAL #
from math_utils.functions import prime_power
from logical.algebra.structure import *

__all__ = [
    'has_identities',
    'is_boolean_algebraic',
    'is_commutative',
    'is_complementary',
    'is_distributive',
    'table',
    'binop_table',
    'unop_table'
]


def is_commutative(struct: Field | Structure) -> bool:
    return all(x + y == y + x and x * y == y * x for x, y in struct.operands(2))


def is_distributive(struct: Field | Structure) -> bool:
    return all(x * (y + z) == (x * y) + (x * z) and x + (y * z) == (x + y) * (x + z)
               for x, y, z in struct.operands(3))


def has_identities(struct: Field | Structure) -> bool:
    return struct[0] is not None and struct[1] is not None


def is_complementary(struct: Field | Structure) -> bool:
    return all(x + -x == struct[1] and x * -x == struct[0] for x in struct.elements)


def is_boolean_algebraic(struct: Field | Structure) -> bool:
    return (is_commutative(struct)
            and is_distributive(struct)
            and has_identities(struct)
            and is_complementary(struct))


def no_zero_dividers(struct: Field | Structure) -> bool:
    return all(a * b != struct[0] for a, b in struct.operands(2) if a != struct[0] and b != struct[0])


def is_finite_field(struct: Field | Structure) -> bool:
    return (prime_power(len(struct.elements)) != (0, 0)
            and is_commutative(struct)
            and has_identities(struct)
            and no_zero_dividers(struct))


def unop_table(struct: Field | Structure, formula: Callable[[...], ...]) -> None:
    """
    Print table for UNARY OPERATIONS on given Structure
    """
    table(struct, formula)


def binop_table(struct: Field | Structure, formula: Callable[[..., ...], ...]) -> None:
    """
    Print table for BINARY OPERATIONS on given Structure
    """
    elems = sorted(struct.elements)
    width = len(str(max(elems)))

    print(' ' * width + ' | ' + '  '.join(str(el).rjust(width) for el in elems))
    print('-' * width + '-+-' + '--'.join(['-' * width] * len(elems)))
    for x in elems:
        print('%s |' % str(x).rjust(width), '  '.join(str(formula(x, y)).rjust(width) for y in elems))


def table(struct: Field | Structure, formula: Callable[..., ...]) -> None:
    """
    Print table for N-ARY OPERATIONS on given Structure
    """
    n = formula.__code__.co_argcount
    width = len(str(max(struct.elements)))
    for operands in struct.operands(n):
        print('%s | %s' % ('  '.join(str(operand).rjust(width) for operand in operands), formula(*operands)))


def doctest_functions() -> None:
    """
    >>> B
    Structure(name='B', set={0, 1}, add=OR, mul=AND, inv=NOT)
    >>> is_boolean_algebraic(B)
    True

    >>> D6 = D(6)
    >>> D6
    Structure(name='D6', set={1, 2, 3, 6}, add=lcm, mul=gcd, inv=floordiv)
    >>> D6.elements
    {D6(1), D6(2), D6(3), D6(6)}
    >>> D6.identity_add
    D6(1)
    >>> D6.identity_mul
    D6(6)
    >>> is_boolean_algebraic(D6)  # commutative, distributive, identities and complementary
    True
    >>> D6(3) + D6(3)
    D6(3)

    >>> D8 = D(8)
    >>> is_commutative(D8)
    True
    >>> is_distributive(D8)
    True
    >>> has_identities(D8)
    True
    >>> is_complementary(D8)
    False
    >>> is_boolean_algebraic(D8)
    False

    >>> import operator

    >>> is_finite_field(Field('Z7', 7, operator.add, operator.mul))
    True
    >>> is_finite_field(Field('Z8', 8, operator.add, operator.mul))
    False
    """


def doctest_tables() -> None:
    """
    >>> import operator

    >>> unop_table(B, formula=operator.neg)
    0 | 1
    1 | 0
    >>> binop_table(B, formula=operator.add)
      | 0  1
    --+-----
    0 | 0  1
    1 | 1  1
    >>> binop_table(B, formula=operator.mul)
      | 0  1
    --+-----
    0 | 0  0
    1 | 0  1
    >>> table(B, formula=lambda x, y, z: x * (y + z) == x * y + x * z) # Distribution Law 1
    0  0  0 | True
    0  0  1 | True
    0  1  0 | True
    0  1  1 | True
    1  0  0 | True
    1  0  1 | True
    1  1  0 | True
    1  1  1 | True
    >>> table(B, formula=lambda x, y, z: x + (y * z) == (x + y) * (x + z)) # Distribution Law 2
    0  0  0 | True
    0  0  1 | True
    0  1  0 | True
    0  1  1 | True
    1  0  0 | True
    1  0  1 | True
    1  1  0 | True
    1  1  1 | True
    >>> unop_table(B, formula=lambda x: x + -x)
    0 | 1
    1 | 1
    >>> unop_table(B, formula=lambda x: x * -x)
    0 | 0
    1 | 0

    >>> D6 = D(6)
    >>> unop_table(D6, formula=operator.neg)
    1 | 6
    2 | 3
    3 | 2
    6 | 1
    >>> binop_table(D6, formula=operator.add)
      | 1  2  3  6
    --+-----------
    1 | 1  2  3  6
    2 | 2  2  6  6
    3 | 3  6  3  6
    6 | 6  6  6  6
    >>> binop_table(D6, formula=operator.mul)
      | 1  2  3  6
    --+-----------
    1 | 1  1  1  1
    2 | 1  2  1  2
    3 | 1  1  3  3
    6 | 1  2  3  6

    >>> D8 = D(8)
    >>> unop_table(D8, formula=operator.neg)
    1 | 8
    2 | 4
    4 | 2
    8 | 1
    >>> binop_table(D8, formula=operator.add)
      | 1  2  4  8
    --+-----------
    1 | 1  2  4  8
    2 | 2  2  4  8
    4 | 4  4  4  8
    8 | 8  8  8  8
    >>> binop_table(D8, formula=operator.mul)
      | 1  2  4  8
    --+-----------
    1 | 1  1  1  1
    2 | 1  2  2  2
    4 | 1  2  4  4
    8 | 1  2  4  8
    >>> D8_0 = D8.identity_add
    >>> D8_1 = D8.identity_mul
    >>> int(D8_0), int(D8_1)
    (1, 8)
    >>> table(D8, lambda x: x + D8_0 == x)
    1 | True
    2 | True
    4 | True
    8 | True
    >>> table(D8, lambda x: x * D8_1 == x)
    1 | True
    2 | True
    4 | True
    8 | True
    >>> table(D8, lambda x: x + -x == D8_1)
    1 | True
    2 | False
    4 | False
    8 | True
    >>> table(D8, lambda x: x * -x == D8_0)
    1 | True
    2 | False
    4 | False
    8 | True

    >>> unop_table(GF7, formula=operator.neg)  # additive inverse
    0 | 0
    1 | 6
    2 | 5
    3 | 4
    4 | 3
    5 | 2
    6 | 1
    >>> table(GF7, formula=lambda x: x ** -1)  # multiplicative inverse
    0 | nan
    1 | 1
    2 | 4
    3 | 5
    4 | 2
    5 | 3
    6 | 6
    >>> binop_table(GF7, formula=operator.add)
      | 0  1  2  3  4  5  6
    --+--------------------
    0 | 0  1  2  3  4  5  6
    1 | 1  2  3  4  5  6  0
    2 | 2  3  4  5  6  0  1
    3 | 3  4  5  6  0  1  2
    4 | 4  5  6  0  1  2  3
    5 | 5  6  0  1  2  3  4
    6 | 6  0  1  2  3  4  5
    >>> binop_table(GF7, formula=operator.mul)
      | 0  1  2  3  4  5  6
    --+--------------------
    0 | 0  0  0  0  0  0  0
    1 | 0  1  2  3  4  5  6
    2 | 0  2  4  6  1  3  5
    3 | 0  3  6  2  5  1  4
    4 | 0  4  1  5  2  6  3
    5 | 0  5  3  1  6  4  2
    6 | 0  6  5  4  3  2  1
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
