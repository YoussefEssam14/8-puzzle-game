"""
A search-tree node: the board state plus everything needed to reconstruct
the path and evaluate the node.

Design rules:
  * frozen  -> safe to hash and push into sets / heaps
  * eq=False + custom __eq__/__hash__ -> identity is the *state only*
  * parent/action/g/h excluded from equality  -> two nodes with the same
    board but different g are "the same node" for visited-set purposes
  * __lt__ gives heapq a total order
"""
from dataclasses import dataclass , field
from typing import Tuple , List , Dict , Optional
from app.common import State



# for bypassing object adress equality and immutability (as two nodes with the same board but different g are "the same node" for visited-set purposes)
@dataclass(eq=False,frozen = True)
class Node:
    state : State
    # parent/action/g/h excluded from equality
    parent : Optional[Node] = field(default = None , compare = False)
    g : int = 0  #cost from start
    h : int = 0  #heuristic
    action : Optional[str] = field(default = None , compare = False)

    # to acess the f = g + h easily using dot operator
    @property
    def f(self) ->float:
        return self.g + self.h;
    
    def __hash__(self)->int:
        return hash(self.state)
    def __eq__(self,other : object)->bool:
        return isinstance(other,Node) and self.state == other.state

    # Total order for heapq: lowest f first; on ties prefer deeper
    # (larger g); final tiebreak on state makes the order deterministic.
    # How it works: first compare f values (lower is better); if they're equal, compare -g (since smaller g means deeper path, we negate it so larger g comes first in the sort); if those are also equal, compare the state tuple itself to ensure a stable, deterministic ordering.
    def __lt__(self,other:'Node') ->bool:
        return (self.f,-self.g,self.state) < (other.f,-other.g,other.state)
    
    # Reconstruct path by walking parent pointers
    def path(self) -> Tuple[List[State], List[str]]:
        states: List[State] = []
        moves: List[str] = []
        cur: Optional[Node] = self

        while cur is not None:
            states.append(cur.state)
            if cur.action is not None:
                moves.append(cur.action)  # BUG-12 fix: was insert(0,...) — O(n²)
            cur = cur.parent

        states.reverse()
        moves.reverse()  # single reverse → O(n), correct order
        return states, moves
    


