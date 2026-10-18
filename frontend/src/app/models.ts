export type Algorithm = 'bfs' | 'dfs' | 'iddfs' | 'astar';
export type Heuristic = 'manhattan' | 'euclidean';
export interface SolveRequest {
  state: number[];
  algorithm?: Algorithm;
  heuristic?: Heuristic;
  max_depth?: number;
  node_limit?: number;
}
export interface SolveResponse {
  algorithm: Algorithm;
  heuristic: Heuristic | null;
  found: boolean;
  solvable: boolean;
  moves: string[];
  path: number[][];
  nodes_expanded: number;
  nodes_generated: number;
  max_frontier: number;
  depth: number;
  path_cost: number;
  time_ms: number;
  optimal: boolean;
  note: string;
}

export interface SolvableRequest {
  state: number[];
}

export interface SolvableResponse {
  solvable: boolean;
}

export interface RandomResponse {
  state: number[];
  solvable: boolean;
}

export interface SampleResponse {
  state: number[];
}