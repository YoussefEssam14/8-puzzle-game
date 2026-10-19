"""
FastAPI wrapper around the 8-puzzle search algorithms.
"""
import random
import os 
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from dotenv import load_dotenv
from app import puzzle
from app.algorithms import solve as run_search
from app.common import SearchResult
from app.models import SolveRequest, SolveResponse , SolvablityCheckRequest , SolvablityCheckResponse
from app.services import _to_response
app = FastAPI(title="8-Puzzle AI Solver", version="1.0.0")
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)
SAMPLE_STATE = [1, 8, 2, 0, 4, 3, 7, 6, 5]
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
        if puzzle.solvable(tuple(s)) == solvable:
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
        ("bfs",   None),
        ("dfs",   None),
        ("iddfs", None),
        ("astar", "manhattan"),
        ("astar", "euclidean"),
    ]
    out : List[SolveResponse] = []

    for algo , heur in configs:
        res = run_search(
            req.state, algo , heur or "manhattan" , req.max_depth,req.node_limit
        )
        out.append(_to_response(res,algo , heur or None))
    return out  
@app.post("/api/solve/solvability",response_model = SolvablityCheckResponse)
def solveable(req : SolvablityCheckRequest):
    return SolvablityCheckResponse(solvable = puzzle.solvable(tuple(req.state)))
    