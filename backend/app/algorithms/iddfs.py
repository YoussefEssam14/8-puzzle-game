import math
import os
import time
from typing import Dict, List

from dotenv import load_dotenv

from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors

load_dotenv()


def iddfs(
    start_state: State,
    max_depth: int = int(os.getenv("DEFAULT_MAX_DEPTH", 31)),
    node_limit: int = int(os.getenv("DEFAULT_NODE_LIMIT", 5_000_000)),
    **_,
) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True, note="IDDFS")

    for limit in range(int(max_depth) + 1):
        best_depth: Dict[State, int] = {}
        stack: List[Node] = [start]

        while stack:
            node = stack.pop()
            if best_depth.get(node.state, math.inf) <= node.g:
                continue
            best_depth[node.state] = node.g

            if stats.expanded >= node_limit:
                return make_result(
                    False, [], [], stats, t0, optimal=False,
                    note=f"Aborted: expansion budget of {node_limit:,} exceeded",
                )
            stats.expanded += 1

            if node.state == GOAL:
                path, moves = node.path()
                return make_result(
                    True, path, moves, stats, t0, optimal=True,
                    note=f"IDDFS solution found at depth={limit}",
                )

            if node.g >= limit:
                continue

            for move, new_state in neighbors(node.state):
                stats.generated += 1
                stack.append(Node(new_state, parent=node, action=move, g=node.g + 1))
                stats.search_depth = max(stats.search_depth,node.g + 1)

            stats.max_frontier = max(stats.max_frontier, len(stack))

    return make_result(
        False, [], [], stats, t0, optimal=False,
        note=f"No solution within depth limit {max_depth}",
    )