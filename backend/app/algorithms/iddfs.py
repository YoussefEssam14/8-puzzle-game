"""Iterative Deepening DFS: optimal, memory-light, re-expansion heavy."""
from __future__ import annotations

import time
from typing import Optional, Set

from app.common import GOAL, SearchResult, Stats, make_result
from app.node import Node
from app.puzzle import neighbors


# raise exception when budget exceed
class BudgetExceeded(Exception):
    pass    

def iddfs(
    start_state : State ,
     max_depth : int = 20,
     node_limit:int=2_000_000
     **_, # to absorb heristic fro solve()
     ) -> SearchResult:


    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path , moves = start.path()
        return make_result(True , path , moves , stats , t0 , optimal = True)
    
    def dls(node:Node , depth : int , limit : int , path_set : Set) -> Optional[Node]:
        if node.state == GOAL:
            return node
        if depth == limit:
            return None

        stats.expanded += 1
        if stats.expanded > node_limit:
            raise BudgetExceeded
    
        for move , new_state in neighbors(node.state):
            if new_state in path_set:
                continue
            stats.generated+=1
            path_set.add(new_state)
            child = Node(new_state , parent=node , action=move , g=node.g+1, h=0)
            found = dls(child, depth + 1, limit, path_set)
            path_set.discard(new_state)
            if found is not None:
                return found
        return None
    
    try:
        for limit in range(max_depth + 1):
            goal_node = dls(start, 0, limit, {start_state})
            stats.max_frontier = max(stats.max_frontier, limit + 1)
            if goal_node is not None:
                path, moves = goal_node.path()
                return make_result(
                    True, path, moves, stats, t0, optimal=True,
                    note=f"Solution found at iteration depth={limit}",
                )
    except BudgetExceeded:
        return make_result(
            False, [], [], stats, t0, optimal=True,
            note=(
                f"Aborted: expansion budget of {node_limit:,} exceeded "
                f"(IDDFS re-expands heavily on hard instances)"
            ),
        )
    return make_result(
        False, [], [], stats, t0, optimal=True,
        note=f"No solution within depth limit {max_depth}",
    )


# if __name__ == "__main__":
#     r = iddfs((1, 2, 5, 3, 4, 0, 6, 7, 8), max_depth=20)
#     print("IDDFS found:", r.found, "| cost:", r.cost,
#           "| expanded:", r.stats.expanded, "| time:", r.time_ms, "ms")
#     print("moves:", r.moves)