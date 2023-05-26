"""
Networks: https://github.com/olooney/circuit/blob/master/README.md
"""
from typing import TypeVar

_T = TypeVar('_T')


# noinspection PyPep8Naming
def TRI_STATE(control):
    """
    >>> TRI_STATE(0)(0)
    >>> TRI_STATE(0)(1)
    >>> TRI_STATE(1)(0)
    0
    >>> TRI_STATE(1)(1)
    1
    """
    if control:
        # noinspection PyPep8Naming
        def tri_state(input_: _T) -> _T:
            return input_
    else:
        # noinspection PyPep8Naming,PyUnusedLocal
        def tri_state(input_: _T) -> None:
            return None
    return tri_state


if __name__ == '__main__':
    import doctest

    doctest.testmod()
