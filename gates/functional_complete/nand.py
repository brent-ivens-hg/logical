"""
NAND: https://en.wikipedia.org/wiki/NAND_logic

Excerpt from wikipedia.com:

    The NAND gate has the property of functional completeness, which it shares with the NOR gate.
    That is, any other logic function (AND, OR, etc.) can be implemented using only NAND gates.

    [source](https://en.wikipedia.org/wiki/NAND_gate#Functional_completeness)
"""
from utils.decorating import cast, multicast


# noinspection PyPep8Naming
@cast
def NAND(A, B):
    """
    NAND Gate

    A: ──|~&
         |~&── OUT: ~(A & B)
    B: ──|~&

    >>> NAND(0, 0)
    1
    >>> NAND(0, 1)
    1
    >>> NAND(1, 0)
    1
    >>> NAND(1, 1)
    0
    """
    return not (A and B)


# noinspection PyPep8Naming,SpellCheckingInspection
@cast
def TNAND(A, B, C):
    """
    TERNARY NAND Using NAND Gates

    A ──|~&  ┌──|~&
        |~&──┤  |~&──┐
    B ──|~&  └──|~&  └──|~&
                        |~&── OUT: ~(A & B & C)
    C ──────────────────|~&


    >>> TNAND(0, 0, 0)
    1
    >>> TNAND(0, 0, 1)
    1
    >>> TNAND(0, 1, 0)
    1
    >>> TNAND(0, 1, 1)
    1
    >>> TNAND(1, 0, 0)
    1
    >>> TNAND(1, 0, 1)
    1
    >>> TNAND(1, 1, 0)
    1
    >>> TNAND(1, 1, 1)
    0
    """
    X = NAND(A, B)
    return NAND(NAND(X, X), C)


# ------------------------ #
#       UNARY GATES        #
# ------------------------ #

# noinspection PyPep8Naming
@cast
def NAND_ID(A):
    """
    NOT Gate Using NAND Gates

         ┌──|~&
    A: ──┤  |~&── OUT: A
         └──|~&

    >>> NAND_NOT(0)
    1
    >>> NAND_NOT(1)
    0
    """
    return NAND(A, A)


# noinspection PyPep8Naming
@cast
def NAND_NOT(A):
    """
    NOT Gate Using NAND Gates

         ┌──|~&
    A: ──┤  |~&── OUT: ~A
         └──|~&

    >>> NAND_NOT(0)
    1
    >>> NAND_NOT(1)
    0
    """
    return NAND(A, A)


# ------------------------ #
#       BINARY GATES       #
# ------------------------ #

# noinspection PyPep8Naming,PyUnusedLocal
@cast
def NAND_CONTRADICTION(A, B):
    """
    CONTRADICTION/FALSE Gate Using NAND Gates

    >>> NAND_CONTRADICTION(0, 0)
    0
    >>> NAND_CONTRADICTION(0, 1)
    0
    >>> NAND_CONTRADICTION(1, 0)
    0
    >>> NAND_CONTRADICTION(1, 1)
    0
    """
    # TODO: Logical_connectives_expressed_with_NAND.png
    return 0

if __name__ == '__main__':
    from utils.drawing import box

    print(box("""\
    
    A **|~&  ***|~&
        |~&***  |~&***
    B **|~&  ***|~&  ***|~&
                        |~&** OUT: ~(A & B & C)
    C ******************|~&
    
    """, char='*'))


# noinspection PyPep8Naming
@cast
def NAND_AND(A, B):
    """
    AND Gate Using NAND Gates

    A: ──|~&  ┌──|~&
         |~&──┤  |~&── OUT: A & B
    B: ──|~&  └──|~&

    >>> NAND_AND(0, 0)
    0
    >>> NAND_AND(0, 1)
    0
    >>> NAND_AND(1, 0)
    0
    >>> NAND_AND(1, 1)
    1
    """
    X = NAND(A, B)
    return NAND(X, X)


# noinspection PyPep8Naming
@cast
def NAND_A_NIMPLY_B(A, B):
    """
    A NIMPLY B Gate Using NAND Gates
    """


# noinspection PyPep8Naming
@cast
def NAND_A(A, B):
    """
    A Gate Using NAND Gates
    """


# noinspection PyPep8Naming
@cast
def NAND_B_NIMPLY_A(A, B):
    """
    B NIMPLY A Gate Using NAND Gates
    """


# noinspection PyPep8Naming
@cast
def NAND_B(A, B):
    """
    B Gate Using NAND Gates
    """


# noinspection PyPep8Naming
@cast
def NAND_XOR(A, B):
    """
    XOR Gate Using NAND Gates


    A: ──┬──────────|~&
         │          |~&──┐
         └──|~&  ┌──|~&  └──|~&
            |~&──┤          |~&── OUT: A^B
         ┌──|~&  └──|~&  ┌──|~&
         │          |~&──┘
    B: ──┴──────────|~&


    >>> NAND_XOR(0, 0)
    0
    >>> NAND_XOR(0, 1)
    1
    >>> NAND_XOR(1, 0)
    1
    >>> NAND_XOR(1, 1)
    0
    """
    X = NAND(A, B)
    return NAND(NAND(A, X), NAND(X, B))


# noinspection PyPep8Naming
@cast
def NAND_OR(A, B):
    """
    OR Gate Using NAND Gates

         ┌──|~&
    A: ──┤  |~&──┐
         └──|~&  └──|~&
                    |~&── OUT: A | B
         ┌──|~&  ┌──|~&
    B: ──┤  |~&──┘
         └──|~&

    >>> NAND_OR(0, 0)
    0
    >>> NAND_OR(0, 1)
    1
    >>> NAND_OR(1, 0)
    1
    >>> NAND_OR(1, 1)
    1
    """
    return NAND(NAND(A, A), NAND(B, B))


# noinspection PyPep8Naming
@cast
def NAND_NOR(A, B):
    """
    NOR Gate Using NAND Gates

         ┌──|~&
    A: ──┤  |~&──┐
         └──|~&  └──|~&  ┌──|~&
                    |~&──┤  |~&── OUT: ~(A | B)
         ┌──|~&  ┌──|~&  └──|~&
    B: ──┤  |~&──┘
         └──|~&


    >>> NAND_NOR(0, 0)
    1
    >>> NAND_NOR(0, 1)
    0
    >>> NAND_NOR(1, 0)
    0
    >>> NAND_NOR(1, 1)
    0
    """
    X = NAND(NAND(A, A), NAND(B, B))
    return NAND(X, X)


# noinspection PyPep8Naming
@cast
def NAND_XNOR(A, B):  # FIXME: _
    """
    XNOR Gate Using NAND Gates


    A: ──┬──────────|~&
         │          |~&──┐
         └──|~&  ┌──|~&  └──|~&  ┌──|~&
            |~&──┤          |~&──┤  |~&── OUT: ~(A^B)
         ┌──|~&  └──|~&  ┌──|~&  └──|~&
         │          |~&──┘
    B: ──┴──────────|~&


    >>> NAND_XNOR(0, 0)
    1
    >>> NAND_XNOR(0, 1)
    0
    >>> NAND_XNOR(1, 0)
    0
    >>> NAND_XNOR(1, 1)
    1
    """
    X = NAND(A, B)
    Y = NAND(NAND(A, X), NAND(X, B))
    return NAND(Y, Y)


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def NAND_NOT_B(A, B):
    """
    NOT B GateUsing NAND Gates
    """


# ┘ ┐ ┌ └ ┤ ┴ ┬ ├ ─ │ ┼


# noinspection PyPep8Naming
@cast
def NAND_NAND(A, B):
    """
    NAND Gate Using NAND Gates



    >>> NAND_NAND(0, 0)
    1
    >>> NAND_NAND(0, 1)
    1
    >>> NAND_NAND(1, 0)
    1
    >>> NAND_NAND(1, 1)
    0
    """
    X = NAND(A, B)
    Y = NAND(X, X)
    return NAND(Y, Y)


# ------------------------ #
#     SELECTIVE GATES      #
# ------------------------ #

# noinspection PyPep8Naming
@cast
def MUX(A, B, S):
    """
    MUX Gate Using NAND Gates

    A: ──────────────────|~&
                 ┌──|~&  |~&──┐
         ┌───────┤  |~&──|~&  └──|~&
    S: ──┤       └──|~&          |~&── OUT: A x B x S
         └──|~&               ┌──|~&
            |~&───────────────┘
    B: ─────|~&

    >>> MUX(0, 0, 0)
    0
    >>> MUX(0, 1, 0)
    0
    >>> MUX(1, 0, 0)
    1
    >>> MUX(1, 1, 0)
    1
    >>> MUX(0, 0, 1)
    0
    >>> MUX(0, 1, 1)
    1
    >>> MUX(1, 0, 1)
    0
    >>> MUX(1, 1, 1)
    1
    """
    return NAND(NAND(A, NAND(S, S)), NAND(S, B))


# noinspection PyPep8Naming
@multicast
def DEMUX(A, S):
    """
    DEMUX Gate Using NAND Gates

    A: ──┬─────────────|~&  ┌──|~&
         │     ┌──|~&  |~&──┤  |~&── OUT: [1]
         │  ┌──┤  |~&──|~&  └──|~&
         │  │  └──|~&
         └─────────────|~&  ┌──|~&
            │          |~&──┤  |~&── OUT: [2]
    S: ─────┴──────────|~&  └──|~&

    >>> DEMUX(0, 0)
    (0, 0)
    >>> DEMUX(0, 1)
    (0, 0)
    >>> DEMUX(1, 0)
    (1, 0)
    >>> DEMUX(1, 1)
    (0, 1)
    """
    X = NAND(A, NAND(S, S))
    Y = NAND(A, S)
    return NAND(X, X), NAND(Y, Y)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
