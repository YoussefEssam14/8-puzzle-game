from fastapi.testclient import TestClient
from app.main import app 
import pytest
client = TestClient(app)

SAMPLE_STATE = [1, 8, 2, 0, 4, 3, 7, 6, 5]
UNSOLVABLE_STATE = [8, 1, 2, 0, 4, 3, 7, 6, 5]
HARDEST_CONFIGURATION = [8,7,6,0,4,1,2,5,3]
def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_sample():
    r = client.get("/api/sample")
    assert r.status_code == 200
    assert r.json() == {"state" : SAMPLE_STATE}

def test_random_state():
    r = client.get("/api/random?solvable=false&seed=123")
    assert r.status_code == 200
    assert r.json()["solvable"] == False
def test_solvablity_check():
    j = client.get("/api/random?solvable=True")
    print(j.json())
    r = client.post("/api/solve/solvability", json={"state" : j.json()["state"]})
    assert r.status_code == 200
    assert r.json() == {"solvable": True}

    j = client.get("/api/random?solvable=False")
    print(j.json())
    r = client.post("/api/solve/solvability", json={"state" : j.json()["state"]})
    assert r.status_code == 200
    assert r.json() == {"solvable": False}

def test_random_same_seed_same_state():
    a = client.get("/api/random?seed=51").json()
    b = client.get("/api/random?seed=51").json()
    assert a == b


@pytest.mark.parametrize("algo,state", [("bfs", SAMPLE_STATE), ("dfs", SAMPLE_STATE), ("iddfs", SAMPLE_STATE), ("astar", SAMPLE_STATE), ("bfs", UNSOLVABLE_STATE), ("dfs", UNSOLVABLE_STATE), ("iddfs", UNSOLVABLE_STATE), ("astar", UNSOLVABLE_STATE)])
def test_solve(algo,state):
    r = client.post("/api/solve",json={
        "state": state,
        "algorithm": algo,
        "heuristic": "manhattan",
        "max_depth" : 31,   
        "node_limit" : 500000
    })
    assert r.status_code == 200 , r.text
    print(r.json())
    if(state == SAMPLE_STATE):
        assert r.json()["found"] == True
    else:
        assert r.json()["found"] == False
def test_hardest_configuration():
    state = HARDEST_CONFIGURATION
    r = client.post("/api/solve",json={
        "state": state,
        "algorithm": "bfs",
        "heuristic": "manhattan",
        "max_depth" : 60,   
        "node_limit" : 500000
    })
    assert r.status_code == 200 , r.text
    assert r.json()["found"] == True
    assert r.json()["depth"] == 31


@pytest.mark.parametrize("state",[SAMPLE_STATE,UNSOLVABLE_STATE,HARDEST_CONFIGURATION])
def test_compare(state):
    r = client.post("/api/solve/compare",json={
        "state" : state,
    })
    if client.post("/api/solve/solvability",json={
        "state" : state
    }).json()["solvable"] == True:
        assert r.status_code == 200
    else:
        assert r.status_code == 400




invalid_states = [
    [1,2,3,4,5,6,7,8],
    [0,1,2,3,4,5,6,7,9],
    [1,2,3],
    [-1,1,2,3,4,5,6,7,8]
]

@pytest.mark.parametrize("state",invalid_states)
def test_invalid_states(state):
    r = client.post("/api/solve",json={
        "state": state,
        "algorithm": "bfs",
        "heuristic": "manhattan",
        "max_depth" : 31,   
        "node_limit" : 500000
    })
    assert r.status_code in [400, 422]
    r = client.post("/api/solve/compare",json={
        "state" : state,
    })
    assert r.status_code in [400,422]
    r = client.post("/api/solve/solvability",json={
        "state" : state,
    })
    assert r.status_code in [400,422]
   

def test_solve_invalid_request():
    r = client.post("/api/solve",json={
        "state" : SAMPLE_STATE,
        "algorithm" : "wtf_i_hate_this_college",
        "heruistic" : "adgkh;fgh",
        "max_depth" : 10001001010,
        "node_limit" : 0
    })
    assert r.status_code in [400,422]
def test_solve_node_limit_exceeded():
    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "iddfs",
        "max_depth" : 31,
        "node_limit" : 1_001
    })
    assert r.status_code == 200

    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : 31,
        "node_limit" : 1_001
    })
    assert r.status_code == 200

    # choosing node limits violating the pydantic schemees
    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : 31,
        "node_limit" :10
    })
    assert r.status_code == 422
    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : 31,
        "node_limit" : 20_000_100
    })
    assert r.status_code == 422
def test_violate_depth_limit():
    r = client.post("/api/solve",json = {
            "state" : HARDEST_CONFIGURATION,
            "algorithm" : "iddfs",
            "max_depth" : 31,
            "node_limit" : 1_001
    })
    assert r.status_code == 200

    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : 31,
        "node_limit" : 1_001
    })
    assert r.status_code == 200

    # choosing depths violating the pydantic schemees
    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : 60,
        "node_limit" :10
    })
    assert r.status_code == 422
    r = client.post("/api/solve",json = {
        "state" : HARDEST_CONFIGURATION,
        "algorithm" : "dfs",
        "max_depth" : -1,
        "node_limit" : 20_000_100
    })
    assert r.status_code == 422


def test_random_invalid_query_parameters():
    r = client.get("/api/random?solvable=maybe")
    assert r.status_code == 422

    r = client.get("/api/random?solvable=true&seed=nan")
    assert r.status_code == 422
def test_invalid_heuristic():
    r = client.post("/api/solve",json={
        "state" : SAMPLE_STATE,
        "algorithm" : "astar",
        "heuristic" : "wtof",
        "max_depth" : 31,
        "node_limit" : 500_000
    })
    assert r.status_code == 422
