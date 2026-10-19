# ```
# Board model , legal moves and solvablity test
# ```

from __future__ import annotations
from typing import  Tuple , List 
from app.common import CELLS , GOAL , N , State


def is_valid(state : State) ->bool:
    return len(state) == CELLS and sorted(state) == GOAL

def is_goal(state : State) ->bool:
    return state == GOAL

def find_blank(state : State) -> int:
    """Return the index of the blank tile (0), or -1 if not found."""
    try:
        return state.index(0)
    except ValueError:
        return -1

def solvable(state : State) -> bool:
    """3x3 puzzle is solvable iff the inversion count of tiles (ignoring 0) is even."""
    tiles = [t for t in state if t != 0]
    inv = sum(
        1
        for i in range(len(tiles))
        for j in range(i+1,len(tiles))
        if tiles[i] > tiles[j]
    )
    return inv%2 == 0

def _swap(state : State , i : int , j : int) -> State:
    lst = list(state)
    lst[i],lst[j] = lst[j],lst[i]
    return tuple(lst)


def neighbors(state : State ) -> List[Tuple[str,State]]:
    i = find_blank(state)
    r , c = divmod(i,N)
    moves = []
    if r > 0:
        moves.append(("UP",_swap(state,i,i-N)))
    if r < N - 1:
        moves.append(("DOWN",_swap(state,i,i+N)))
    if c > 0:
        moves.append(("LEFT",_swap(state,i,i-1)))
    if c < N - 1:
        moves.append(("RIGHT",_swap(state,i,i+1)))
    return moves
    

    
