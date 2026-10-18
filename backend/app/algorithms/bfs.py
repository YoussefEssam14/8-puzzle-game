"""Breadth-First Search: complete, optimal, memory-hungry."""
from __future__ import annotations

import time
from collections import deque
from typing import Deque, Set

from app.common import GOAL, SearchResult, Stats, make_result
from app.node import Node
from app.puzzle import neighbors


def bfs(start_state: tuple, **_) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True)

    visited: Set = {start_state} # already visited nodes
    frontier: Deque[Node] = deque([start]) # our frontier which is a queue in a bfs exploring level by level
    stats.max_frontier = 1 # max number of nodes contained in the frontier at a time

    while frontier: # while the frontier have unexplored nodes
        node = frontier.popleft() # pop the node with the lowest depth
        stats.expanded += 1

        # explore neighbors of current state
        for move, new_state in neighbors(node.state):
            if new_state in visited:
                continue
            visited.add(new_state)
            stats.generated += 1
            child = Node(new_state, parent=node, action=move, g=node.g + 1,h = 0)

            if new_state == GOAL:
                path, moves = child.path()
                return make_result(True, path, moves, stats, t0, optimal=True)

            frontier.append(child)

        stats.max_frontier = max(stats.max_frontier, len(frontier))

    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")


# if __name__ == "__main__":
#     r = bfs((1, 2, 5, 3, 4, 0, 6, 7, 8))
#     print("BFS  found:", r.found, "| cost:", r.cost,
#           "| expanded:", r.stats.expanded, "| time:", r.time_ms, "ms")
#     print("moves:", r.moves)