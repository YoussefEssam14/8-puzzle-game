"""Depth-First Search: depth-limited, non-optimal, cycle-safe."""
from __future__ import annotations

import time
from typing import FrozenSet, List, Tuple

from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors


def dfs(start_state: State, max_depth: int = 31, **_) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True)

    frontier: List[Tuple[Node, int, FrozenSet[State]]] = [
        (start, 0, frozenset({start_state}))
    ]
    stats.max_frontier = 1

    while frontier:
        node, depth, path_set = frontier.pop()
        stats.expanded += 1

        if node.state == GOAL:
            path, moves = node.path()
            return make_result(
                True, path, moves, stats, t0, optimal=False,
                note=f"DFS solution of length {len(moves)} (not optimal)",
            )

        # Prune deeper branches
        if depth >= max_depth:
            continue

        # Explore neighbors of current state
        for move, new_state in neighbors(node.state):
            if new_state in path_set:   # cycle on current path only
                continue
            stats.generated += 1
            child = Node(new_state, parent=node, action=move, g=node.g + 1, h=0)
            frontier.append((child, depth + 1, path_set | {new_state}))

        stats.max_frontier = max(stats.max_frontier, len(frontier))

    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")


# if __name__ == "__main__":
#     r = dfs((1, 2, 5, 3, 4, 0, 6, 7, 8), max_depth=31)
#     print("DFS found:", r.found, "| cost:", r.cost,
#           "| expanded:", r.stats.expanded, "| time:", r.time_ms, "ms")
#     print("moves:", r.moves)