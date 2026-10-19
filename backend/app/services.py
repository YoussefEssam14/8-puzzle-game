from app.common import SearchResult
from app.models import  SolveResponse 
from typing import Optional
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