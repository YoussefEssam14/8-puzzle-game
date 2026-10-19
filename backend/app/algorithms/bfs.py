"""Breadth-First Search: complete, optimal, memory-hungry."""
import time
from collections import deque
from typing import Deque, Set

from app.common import GOAL, SearchResult, State, Stats, make_result
from app.node import Node
from app.puzzle import neighbors


def bfs(start_state: State, **_) -> SearchResult:
    t0 = time.perf_counter()
    stats = Stats()
    start = Node(start_state)

    if start_state == GOAL:
        path, moves = start.path()
        return make_result(True, path, moves, stats, t0, optimal=True)

    visited: Set = {start_state} # already visited nodes
    queue: Deque[Node] = deque([start]) # our frontier which is a queue in a bfs exploring level by level
    stats.max_frontier = 1 # max number of nodes contained in the frontier at a time

    while queue: # while the queue have unexplored nodes
        node = queue.popleft() # pop the node with the lowest depth
        stats.expanded += 1


        # explore neighbors of current state
        for move, new_state in neighbors(node.state):
            if new_state in visited:
                continue
            visited.add(new_state)
            stats.generated += 1
            child = Node(new_state, parent=node, action=move, g=node.g + 1, h=0)
            if new_state == GOAL:
                path, moves = child.path()
                stats.max_frontier = max(stats.max_frontier, len(queue))
                return make_result(True, path, moves, stats, t0, optimal=True , note = "BFS")

            queue.append(child)
        stats.max_frontier = max(stats.max_frontier, len(queue))
    return make_result(False, [], [], stats, t0, optimal=False, note="Unsolvable")

