"""Algorithm registry + unified `solve()` entry point."""

from app.algorithms.astar import astar
from app.algorithms.bfs import bfs
from app.algorithms.dfs import dfs
from app.algorithms.iddfs import iddfs
from app.common import SearchResult, State, Stats
from app.puzzle import solvable


ALGORITHMS = {
    "bfs" : bfs,
    "dfs" : dfs,
    "iddfs" : iddfs,
    "astar" : astar
}

def solve(
    state : State,
    algorithm : str = "astar",
    heuristic : str = "manhattan",
    max_depth : int = 31, # theoretical max depth that can reached
    node_limit : int = 2_000_000
) -> SearchResult:
    state = tuple(state)
    if not solvable(state):
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

    return ALGORITHMS[algorithm](
        state,
        heuristic = heuristic,
        max_depth = int(max_depth),
        node_limit = int(node_limit),
    )
