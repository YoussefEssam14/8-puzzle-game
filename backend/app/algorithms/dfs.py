import os
import time
from typing import List, Set
from dotenv import load_dotenv
from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors

load_dotenv()

def dfs(start_state: State,
        node_limit: int = int(os.getenv("DEFAULT_NODE_LIMIT", 2_000_000)),
        **_) -> SearchResult:    
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True, note="DFS")

    stack: List[Node] = [start]          
    visited: Set[State] = {start_state} 
    stats.max_frontier = 1

    while stack:
        node = stack.pop()
        stats.expanded += 1

        if node.state == GOAL:
            path, moves = node.path()
            return make_result(True, path, moves, stats, t0, optimal=False,
                               note=f"DFS solution of length {len(moves)} (not optimal)")

        if stats.expanded > node_limit:
            return make_result(False, [], [], stats, t0, optimal=False,
                               note=f"Aborted: node budget of {node_limit:,} exceeded")

        for move, new_state in neighbors(node.state):
            if new_state in visited:
                continue
            visited.add(new_state)
            stats.generated += 1
            stack.append(Node(new_state, parent=node, action=move, g=node.g + 1))
            stats.search_depth = max(stats.search_depth, node.g + 1)

        stats.max_frontier = max(stats.max_frontier, len(stack))

    return make_result(False, [], [], stats, t0, optimal=False,
                       note="Unsolvable") 