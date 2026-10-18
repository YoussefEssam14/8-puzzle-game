"""A*: optimal with an admissible + consistent heuristic."""
from __future__ import annotations

import heapq
import math
import time
from typing import Dict, Set

from app.common import GOAL, SearchResult, State, Stats, make_result
from app.heuristics import HEURISTICS
from app.node import Node
from app.puzzle import neighbors


def astar(start_state: State, heuristic: str = "manhattan", **_) -> SearchResult:
    h = HEURISTICS[heuristic]
    t0 = time.perf_counter()
    stats = Stats()


    start = Node(start_state,g=0,h=h(start_state))
    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True)

    best_g : Dict = {start_state:0} # map each state to it's best explored g_value
    closed : Set = set() # states already visiteds
    open_heap: List[Node] = [start]  # BUG-10 fix: was bare List
    stats.max_frontier = 1

    while open_heap:
        node = heapq.heappop(open_heap) # pop the node with the lowest f = g+h
        if node.state in closed:
            continue
        closed.add(node.state)
        stats.expanded+=1

        if node.state == GOAL: # goal node is reached
            path, moves = node.path()
            return make_result(
                True, path, moves, stats, t0, optimal=True,
                note=f"A* with {heuristic} heuristic",
            )
        # explore neighbors of current state 
        for move, new_state in neighbors(node.state):
            if new_state in closed:
                continue
            g = node.g + 1 # next state g cost
            if g < best_g.get(new_state,math.inf): # stale state
                best_g[new_state] = g
                stats.generated+=1
                heapq.heappush(
                    open_heap,
                    Node(
                        new_state,
                        parent = node,
                        action = move,
                        g = g,
                        h = h(new_state)
                    ),
                )
        stats.max_frontier = max(stats.max_frontier,len(open_heap))

    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")  


# if __name__ == "__main__":
#     for name in ("manhattan", "euclidean"):
#         r = astar((1, 2, 5, 3, 4, 0, 6, 7, 8), heuristic=name)
#         print(f"A*({name})  found:", r.found, "| cost:", r.cost,
#                 "| expanded:", r.stats.expanded, "| time:", r.time_ms, "ms")
#         print("  moves:", r.moves)