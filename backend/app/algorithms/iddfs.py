"""Iterative Deepening DFS: optimal, memory-light, re-expansion heavy."""
import time
from typing import Set  , Optional
from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors
import os
from dotenv import load_dotenv
load_dotenv()

class BudgetExceeded(Exception):
    def __init__(self, node_limit: int):
        self.node_limit = node_limit

    def __str__(self):
        return f"Aborted: expansion budget of {self.node_limit:,} exceeded (IDDFS re-expands heavily on hard instances)"


def iddfs(
    start_state: State,
    max_depth: int = int(os.getenv("DEFAULT_MAX_DEPTH")),
    node_limit: int = int(os.getenv("DEFAULT_NODE_LIMIT")),
    **_,
) -> SearchResult:

    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True , note="IDDFS")

    def dls(
        node: Node,
        depth: int,
        limit: int,
        path_set: Set[State], 
    ) -> Optional[Node]:
        if node.state == GOAL:
            return node
        if depth >= limit:
            return None

        stats.expanded += 1
        if stats.expanded > node_limit:
            raise BudgetExceeded(node_limit)

        for move, new_state in neighbors(node.state):
            if new_state in path_set:
                continue
            stats.generated += 1
            child = Node(new_state, parent=node, action=move, g=node.g + 1, h=0)
            path_set.add(new_state)
            found = dls(child, depth + 1, limit, path_set)
            path_set.remove(new_state)
            if found is not None:
                return found
        return None

    try:
        for limit in range(int(max_depth) + 1):
            stats.max_frontier = max(stats.max_frontier, limit + 1)
            goal_node = dls(start, 0, limit, {start_state})
            if goal_node:
                path, moves = goal_node.path()
                return make_result(
                    True, path, moves, stats, t0, optimal=True,
                    note=f"IDDFS solution found at depth={limit}",
                )
    except BudgetExceeded:
        return make_result(
            False, [], [], stats, t0, optimal=False,
            note=(f"Aborted: expansion budget of {node_limit:,} exceeded")
        )

    return make_result(
        False, [], [], stats, t0, optimal=False, 
        note=f"No solution within depth limit {max_depth}",
    )
