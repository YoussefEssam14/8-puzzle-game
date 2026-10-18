"""Algorithm registry + unified `solve()` entry point."""


from __future__ import annotations
from typing import List



from app.algorithms.astar import astar
from app.algorithms.bfs import bfs
from app.algorithms.dfs import dfs
from app.algorithms.iddfs import iddfs
from app.common import SearchResult, State, Stats
from app.puzzle import solvable


ALGOS = {
    "bfs" : bfs,
    "dfs" : dfs,
    "iddfs" : iddfs,
    "astar" : astar
}

def solve(
    state : State,
    algorithm : str = "astar",
    heuristic : str = "manhattan",
    max_depth : int = 31,
    node_limit : int = 2_000_000
) -> SearchResult:
    start: State = tuple(state) 
    if not solvable(start):
        return SearchResult(
            found=False,
            path=[],
            moves=[],
            stats=Stats(),
            note=(
                "Unsolvable state: odd number of inversions "
                "(no sequence of moves can reach the goal)."
            ),
        )

    return ALGOS[algorithm](
        start,
        heuristic = heuristic,
        max_depth = max_depth,
        node_limit = node_limit,
    )
if __name__ == "__main__":
    import sys
    sample = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    for name in ALGOS:
        r = solve(sample, name)
        print(f"{name:6} -> found={r.found} cost={r.cost} "
              f"expanded={r.stats.expanded} time={r.time_ms:.2f}ms")