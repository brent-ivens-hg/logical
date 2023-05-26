"""
Binary Gates
"""
from utils.decorating import cast

__all__ = [
    'A',
    'AND',
    'A_IMPLY_B',
    'A_NIMPLY_B',
    'B',
    'B_IMPLY_A',
    'B_NIMPLY_A',
    'CONTRADICTION',
    'GATES',
    'NAND',
    'NOR',
    'NOT_A',
    'NOT_B',
    'OR',
    'TAUTOLOGY',
    'XNOR',
    'XOR'
]


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def CONTRADICTION(a, b):
    """
    CONTRADICTION Gate
    """
    return False


# noinspection PyPep8Naming
@cast
def AND(a, b):
    """
    AND Gate
    """
    return a and b


# noinspection PyPep8Naming
@cast
def A_NIMPLY_B(a, b):
    """
    A NIMPLY B Gate
    """
    return a and not b


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def A(a, b):
    """
    A Gate
    """
    return a


# noinspection PyPep8Naming
@cast
def B_NIMPLY_A(a, b):
    """
    B NIMPLY A Gate
    """
    return not a and b


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def B(a, b):
    """
    B Gate
    """
    return b


# noinspection PyPep8Naming
@cast
def XOR(a, b):
    """
    XOR Gate
    """
    return a != b


# noinspection PyPep8Naming
@cast
def OR(a, b):
    """
    OR Gate
    """
    return a or b


# noinspection PyPep8Naming
@cast
def NOR(a, b):
    """
    NOR Gate
    """
    return not (a or b)


# noinspection PyPep8Naming
@cast
def XNOR(a, b):
    """
    XNOR Gate
    """
    return a == b


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def NOT_B(a, b):
    """
    NOT B Gate
    """
    return not b


# noinspection PyPep8Naming
@cast
def B_IMPLY_A(a, b):  # NOTE: converse implication
    """
    B IMPLY A Gate
    """
    return a or not b


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def NOT_A(a, b):
    """
    NOT A Gate
    """
    return not a


# noinspection PyPep8Naming
@cast
def A_IMPLY_B(a, b):
    """
    A IMPLY B Gate
    """
    return not a or b


# noinspection PyPep8Naming
@cast
def NAND(a, b):
    """
    NAND Gate
    """
    return not (a and b)


# noinspection PyPep8Naming,PyUnusedLocal
@cast
def TAUTOLOGY(a, b):
    """
    TAUTOLOGY Gate
    """
    return True


GATES = {  # key = output produced by gate (w/ binary ordered vars)
    0b0000: CONTRADICTION,
    0b0001: AND,
    0b0010: A_NIMPLY_B,
    0b0011: A,
    0b0100: B_NIMPLY_A,
    0b0101: B,
    0b0110: XOR,
    0b0111: OR,
    0b1000: NOR,
    0b1001: XNOR,
    0b1010: NOT_B,
    0b1011: B_IMPLY_A,
    0b1100: NOT_A,
    0b1101: A_IMPLY_B,
    0b1110: NAND,
    0b1111: TAUTOLOGY
}

if __name__ == '__main__':
    FALSE = CONTRADICTION
    TRUE = TAUTOLOGY

    GE = B_IMPLY_A  # equiv. to >= for booleans
    GT = A_NIMPLY_B  # equiv. to >  for booleans
    LE = A_IMPLY_B  # equiv. to <= for booleans
    LT = B_NIMPLY_A  # equiv. to <  for booleans
