# 8-Puzzle Solver

An interactive 8-puzzle solver and visualizer. The application allows users to play the game manually, generate random boards, test solvability, solve configurations using various search algorithms, step through moves, and compare algorithm performance metrics.

## Tech Stack

- Backend: FastAPI, Python, Uvicorn, Pydantic
- Frontend: Angular, TypeScript, Bootstrap

## Implemented Algorithms

The backend implements both uninformed and informed search strategies:

- Breadth-First Search (BFS): Explores nodes level by level. Guarantees an optimal solution (shortest path in number of moves).
- Depth-First Search (DFS): Explores as deep as possible along each branch before backtracking. Memory-efficient, but does not guarantee the shortest path.
- Iterative Deepening DFS (IDDFS): Combines the minimal memory usage of DFS with the optimality of BFS by searching to increasing depth limits.
- A* Search: Best-first informed search algorithm using `f(n) = g(n) + h(n)`. Supports two admissible heuristic functions:
  - Manhattan Distance: Sum of vertical and horizontal distances between current tile positions and goal positions.
  - Euclidean Distance: Straight-line distance between current tile positions and goal positions.

### Solvability Check

A board configuration is solvable if and only if the number of inversions in the state array (excluding the empty tile `0`) is even. Unsolvable states are rejected before running search algorithms to avoid unnecessary computation.

## Project Structure

```
8-puzzle-game/
├── backend/
│   ├── app/
│   │   ├── algorithms/     # BFS, DFS, IDDFS, A*
│   │   ├── heuristics.py   # Manhattan and Euclidean functions
│   │   ├── main.py         # FastAPI routes and middleware
│   │   ├── models.py       # Pydantic schemas
│   │   ├── puzzle.py       # Board representation and move generation
│   │   └── services.py     # Response transformations
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/app/            # Angular components, services, and board logic
    └── package.json
```

## Running the Project

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher and npm

### 1. Backend Setup

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Verify or create `backend/.env`:

```env
PORT=8000
HOST=127.0.0.1
CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
DEFAULT_MAX_DEPTH=31
DEFAULT_NODE_LIMIT=5000000
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The server runs at `http://127.0.0.1:8000`. Swagger documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

From the repository root:

```bash
cd frontend
npm install
npm start
```

The frontend application runs at `http://localhost:4200`.

## API Overview

- `GET /api/health` - Server health check.
- `GET /api/sample` - Retrieve a predefined sample board state.
- `GET /api/random` - Generate a random puzzle state (`solvable` query param supported).
- `POST /api/solve` - Solve a state using the specified algorithm and heuristic.
- `POST /api/solve/compare` - Run all algorithms on the given state and return comparative benchmark metrics.
- `POST /api/solve/solvability` - Verify if a given 8-puzzle state is solvable.
