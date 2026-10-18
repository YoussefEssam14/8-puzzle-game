"""
FastAPI wrapper around the 8-puzzle search algorithms.

Run from `backend/`:
    uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""


from __future__ import annotations
import random
import os 
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from dotenv import load_dotenv

load_dotenv()

from app import puzzle
from app.algorithms import solve as run_search
from app.common import SearchResult
from app.models import SolveRequest, SolveResponse

app = FastAPI(title="8-Puzzle AI Solver", version="1.0.0")

# Angular dev server runs on :4200 — must be allowed to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)



# A famously hard 8-puzzle instance (has 31 moves)
SAMPLE_STATE = [1, 8, 2, 0, 4, 3, 7, 6, 5]
GOAL = puzzle.GOAL

def _to_response(
    res: SearchResult, algorithm: str, heuristic: Optional[str],
) -> SolveResponse:
    return SolveResponse(
        algorithm=algorithm,
        heuristic=heuristic if algorithm == "astar" else None,
        found=res.found,
        solvable=res.found or "Unsolvable" not in res.note,
        moves=res.moves,
        path=[list(s) for s in res.path], 
        nodes_expanded=res.stats.expanded,    
        nodes_generated=res.stats.generated,
        max_frontier=res.stats.max_frontier,
        depth=res.depth,
        path_cost=res.cost,
        time_ms=res.time_ms,
        optimal=res.optimal,
        note=res.note,
    )

@app.get("/api/health", tags=["health"])
def health():
    return {"status" : "ok"}


@app.get('/api/sample')
def sample():
    return {'state' : SAMPLE_STATE}


@app.get('/api/random')
def random_state(solvable : bool = True , seed : Optional[int] = None):
    rnd = random.Random(seed)
    while True:
        s = list(range(9))
        rnd.shuffle(s)
        if not solvable or puzzle.solvable(tuple(s)):
            return {"state" : s,"solvable" : puzzle.solvable(tuple(s))}

@app.post("/api/solve",response_model = SolveResponse)
def solve(req : SolveRequest):
    res = run_search(
        req.state,
        req.algorithm,
        req.heuristic,
        req.max_depth,
        req.node_limit
    )
    return _to_response(res,req.algorithm,req.heuristic)

@app.post("/api/solve/compare", response_model=List[SolveResponse])
def compare(req : SolveRequest):
    if not puzzle.solvable(tuple(req.state)):
        raise HTTPException(status_code=400, detail="State is not solvable.")
    configs = [
        ("bfs",   None,        req.max_depth),
        ("dfs",   None,        req.max_depth),
        ("iddfs", None,        min(req.max_depth, 20)),
        ("astar", "manhattan", req.max_depth),
        ("astar", "euclidean", req.max_depth),
    ]
    out : List[SolveResponse] = []

    for algo , heur , depth in configs:
        res = run_search(
            req.state, algo , heur or "manhattan" , depth,req.node_limit
        )
        out.append(_to_response(res,algo , heur or None))
    return out  