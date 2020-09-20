"""
mathematicalRounding.py

Created on 2020-09-20
Updated on 2020-09-20

Copyright Ryan Kan 2020

Description: Implements mathematical rounding.
"""

# IMPORTS
import math
from decimal import Decimal


# FUNCTIONS
def ceiling(n, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("Decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("Decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(n)

    factor = 10 ** decimals
    return math.ceil(Decimal(n) * factor) / factor


def floor(n, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("Decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(n)

    factor = 10 ** decimals
    return math.floor(Decimal(n) * factor) / factor


def mathematical_round(n, decimals=0):
    n = Decimal(n)
    floor_val = floor(n, decimals=decimals)
    ceiling_val = ceiling(n, decimals=decimals)
    halfway = (floor_val + ceiling_val) / 2

    if n < halfway:
        return floor_val
    else:
        return ceiling_val


# DEBUG CODE
if __name__ == "__main__":
    print(round(0.5625, 3))
    print(mathematical_round(0.5625, 3))

