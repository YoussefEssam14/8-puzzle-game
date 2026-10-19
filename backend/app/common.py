"""Shared types, common utilities, constants and result helpers for the solver.

State encoding: a 9-tuple of ints, row-major, 0 = blank.
Goal: (0, 1, 2, 3, 4, 5, 6, 7, 8)  ->  the goal index of tile v is simply v.

"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Tuple

State = Tuple[int, ...]
GOAL: State = (0, 1, 2, 3, 4, 5, 6, 7, 8)
N = 3
CELLS = N * N


@dataclass
class Stats:
    """Counters accumulated during a search."""
    expanded: int = 0        # states popped from the frontier
    generated: int = 0       # successors pushed onto the frontier
    max_frontier: int = 0    # peak frontier size


@dataclass
class SearchResult:
    found: bool
    path: List[State]
    moves: List[str]
    stats: Stats
    cost: int = 0
    time_ms: float = 0.0
    optimal: bool = False
    note: str = ""

    @property
    def depth(self) -> int:
        """Solution depth = number of moves. Derived, cannot drift."""
        return len(self.moves)


def make_result(
    found: bool,
    path: List[State],
    moves: List[str],
    stats: Stats,
    t0: float,
    optimal: bool,
    note: str = "",
) -> SearchResult:
    """Bundle a finished search into a SearchResult.

    Unit step cost: path cost == number of moves == solution depth.
    """
    return SearchResult(
        found=found,
        path=path,
        moves=moves,
        stats=stats,
        cost=len(moves),
        time_ms=round((time.perf_counter() - t0) * 1000.0, 3),
        optimal=optimal,
        note=note,
    )