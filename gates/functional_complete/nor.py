"""
NOR: https://en.wikipedia.org/wiki/NOR_logic

Excerpt from wikipedia.com:

    The NOR gate has the property of functional completeness, which it shares with the NAND gate.
    That is, any other logic function (AND, OR, etc.) can be implemented using only NOR gates.

    [source](https://en.wikipedia.org/wiki/NOR_gate#Functional_completeness)
"""
from utils.decorating import cast


@cast
def NOR(A, B):
    """
    NAND Gate

    A: ──│~&
         │~&── Y: ~(A & B)
    B: ──│~&

    >>> NOR(0, 0)
    1
    >>> NOR(0, 1)
    0
    >>> NOR(1, 0)
    0
    >>> NOR(1, 1)
    0
    """
    return not (A or B)


# TODO: https://en.wikipedia.org/wiki/NOR_logic


if __name__ == '__main__':
    import doctest

    doctest.testmod()
