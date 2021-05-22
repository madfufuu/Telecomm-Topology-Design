"""
utils.py
    Module that contains the utility function definitions.
"""

import math


def euclidean_distance(p, q):
    return round(
                    math.sqrt(
                        math.pow((q[0] - p[0]), 2) + math.pow((q[1] - p[1]), 2)
                    ),
                    2
                )
