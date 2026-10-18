"""Depth-First Search: depth-limited, non-optimal, cycle-safe."""
import time
from typing import List, Set, Tuple

from app.common import GOAL, SearchResult, Stats, make_result
from app.node import Node
from app.puzzle import neighbors


def dfs(start_state : State , max_depth : int = 31) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path , moves = start.path()
        return make_result(True , path , moves , stats , t0 , optimal = True)
    
    visited : Set[State] = {start_state} # already visited nodes
    frontier : List[Tuple[Node,int]] = [(start,0)] # our frontier which is a stack in a dfs exploring depth by depth
    stats.max_frontier = 1 # max number of nodes contained in the frontier at a time

    while frontier: # while the frontier have unexplored nodes
        node , depth = frontier.pop() # pop the node with the lowest depth
        stats.expanded +=1 

        if node.state == GOAL:
            path, moves = node.path()
            return make_result(
                True, path, moves, stats, t0, optimal=False,
                note=f"DFS solution of length {len(moves)} (not optimal)",
            )
        
        # prune larger depths
        if depth >= max_depth:
            continue    
        # explore neighbors of current state
        for move , new_state in neighbors(node.state):
            if new_state in visited: # if the neighbor is already visited
                continue
            visited.add(new_state)
            stats.generated +=1
            child = Node(new_state, parent=node, action=move, g=node.g+1, h=0)
            frontier.append((child, depth + 1))
        stats.max_frontier = max(stats.max_frontier, len(frontier))
    
    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")


# if __name__ == "__main__":
#     r = dfs((1, 2, 5, 3, 4, 0, 6, 7, 8), max_depth=31)
#     print("DFS found:", r.found, "| cost:", r.cost,
#           "| expanded:", r.stats.expanded, "| time:", r.time_ms, "ms")
#     print("moves:", r.moves)