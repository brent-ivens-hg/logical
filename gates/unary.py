"""
Unary Gates
"""
from utils.decorating import cast

__all__ = ['NOT', 'ID']


# noinspection PyPep8Naming
@cast
def ID(a):
    """
    ID Gate
    """
    return a


# noinspection PyPep8Naming
@cast
def NOT(a):
    """
    NOT Gate
    """
    return not a
