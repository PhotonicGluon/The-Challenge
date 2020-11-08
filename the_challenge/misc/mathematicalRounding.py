"""
mathematicalRounding.py

Created on 2020-09-20
Updated on 2020-11-08

Copyright Ryan Kan 2020

Description: Implements mathematical rounding.
"""

# IMPORTS
import math
from decimal import Decimal


# FUNCTIONS
def ceiling(n, decimals=0):
    """
    Rounds up the number `n` to the specified number of decimal places.

    Args:
        n (Union[int, float]):  The number to be rounded up.

        decimals (int):         The number of decimal places to be rounded up to.
                                (Default = 0)

    Returns:
        Union[int, float]:  The rounded up version of the number `n`.

    Raises:
        TypeError:  If `decimals` is NOT an integer.

        ValueError: If `decimals` is less than 0.

    Examples:
        >>> ceiling(1.2345, 0)
        2
        >>> ceiling(1.2345, decimals=3)
        1.235
        >>> ceiling(-1, decimals=0)
        -1
        >>> ceiling(-3.14159, decimals=0)
        -3
    """

    if not isinstance(decimals, int):
        raise TypeError("Decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("Decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(n)

    factor = 10 ** decimals
    return math.ceil(Decimal(n) * factor) / factor


def floor(n, decimals=0):
    """
    Rounds down the number `n` to the specified number of decimal places.

    Args:
        n (Union[int, float]):  The number to be rounded down.

        decimals (int):         The number of decimal places to be rounded down to.
                                (Default = 0)

    Returns:
        Union[int, float]:  The rounded down version of the number `n`.

    Raises:
        TypeError:  If `decimals` is NOT an integer.

        ValueError: If `decimals` is less than 0.

    Examples:
        >>> floor(1.2345, 0)
        1
        >>> floor(1.2345, decimals=3)
        1.234
        >>> floor(-1, decimals=0)
        -1
        >>> floor(-3.14159, decimals=0)
        -4
    """

    if not isinstance(decimals, int):
        raise TypeError("Decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(n)

    factor = 10 ** decimals
    return math.floor(Decimal(n) * factor) / factor


def mathematical_round(n, decimals=0):
    """
    Rounds the number `n` mathematically. That is, it does not follow Python's banker's rounding, but rather follows
    "mathematical rounding" (i.e. follows "round half up" rules)

    Args:
        n (Union[int, float]):  The number to be rounded.

        decimals (int):         The number of decimal places the number should be rounded to.
                                (Default = 0)

    Returns:
        Union[int, float]:  The rounded version of the number `n`.

    Raises:
        TypeError:  If `decimals` is NOT an integer.

        ValueError: If `decimals` is less than 0.

    Examples:
        >>> round(0.5)
        0
        >>> mathematical_round(0.5)
        1
        >>> round(1.5)
        2
        >>> mathematical_round(1.5)
        2
        >>> round(0.5625, ndigits=3)
        0.562
        >>> mathematical_round(0.5625, decimals=3)
        0.563
        >>> round(0.5635, ndigits=3)
        0.564
        >>> mathematical_round(0.5635, decimals=3)
        0.564
    """

    n = Decimal(n)
    floor_val = floor(n, decimals=decimals)
    ceiling_val = ceiling(n, decimals=decimals)
    halfway = (floor_val + ceiling_val) / 2

    if n < halfway:
        return floor_val
    else:
        return ceiling_val
