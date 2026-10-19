"""Depth-First Search: depth-limited, non-optimal, cycle-safe."""

import time
from typing import Set, List, Tuple
from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors
from dotenv import load_dotenv
import os
load_dotenv()

def dfs(start_state: State, max_depth: int = int(os.getenv("DEFAULT_MAX_DEPTH")), **_) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True, note="DFS")

    # node , depth , set
    stack: List[Tuple[Node, int, Set[State]]] = [
        (start, 0, {start_state})
    ]
    stats.max_frontier = 1

    while stack:
        node, depth, path_set = stack.pop()
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
            stack.append((child, depth + 1, path_set | {new_state}))

        stats.max_frontier = max(stats.max_frontier, len(stack))

    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")
