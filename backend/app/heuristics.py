"""Admissible heuristics for A*."""


from __future__ import annotations
from app.common import N , State

import math


def manhattan(state: State) -> int:
    """Sum of |dr| + |dc| between each tile and its goal cell. Blank ignored."""
    h = 0
    for idx, tile in enumerate(state):
        if tile == 0:  
            continue
        r, c = divmod(idx, N)
        gr, gc = divmod(tile, N)
        h += abs(r - gr) + abs(c - gc)
    return h

def euclidean(state: State) -> float:
    """Sum of straight-line distances between each tile and its goal cell. Blank ignored."""
    h = 0.0
    for idx, tile in enumerate(state):
        if tile == 0:   
            continue
        r, c = divmod(idx, N)
        gr, gc = divmod(tile, N)
        h += math.sqrt((r - gr) ** 2 + (c - gc) ** 2)
    return h

HEURISTICS = {
    "manhattan": manhattan,
    "euclidean": euclidean,
}
