"""Pydantic request/response schemas for the API."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator
import os
from dotenv import load_dotenv
load_dotenv()
Algorithm = Literal["bfs", "dfs", "iddfs", "astar"]
Heuristic = Literal["manhattan", "euclidean"]
class SolveRequest(BaseModel):
    """Incoming solve request — validates the board and the algorithm name."""
    state: List[int] = Field(..., min_length=9, max_length=9)
    algorithm: Algorithm = "astar"
    heuristic: Heuristic = "manhattan"
    max_depth: int = Field(os.getenv("DEFAULT_MAX_DEPTH"), ge=1, le=60)
    node_limit: int = Field(os.getenv("DEFAULT_NODE_LIMIT"), ge=1_000, le=20_000_000)

    @field_validator("state")
    @classmethod
    def _check_permutation(cls, v: List[int]) -> List[int]:
        if sorted(v) != list(range(9)):
            raise ValueError("state must be a permutation of 0..8")
        return v
class SolveResponse(BaseModel):
    """Outgoing solve result — exactly what Angular expects."""
    algorithm: str
    heuristic: Optional[str]
    found: bool
    solvable: bool
    moves: List[str]
    path: List[List[int]]
    nodes_expanded: int
    nodes_generated: int
    max_frontier: int
    depth: int
    path_cost: int
    time_ms: float
    optimal: bool
    note: str
class SolvablityCheckRequest(BaseModel):
    state : List[int] = Field(...,min_length=9,max_length=9)
    @field_validator("state")
    @classmethod
    def _check_permutation(cls,v:List[int]) -> List[int]:
        if sorted(v) != list(range(9)):
            raise ValueError("state must be a permutation of 0..8")
        return v
class SolvablityCheckResponse(BaseModel):
    solvable : bool
