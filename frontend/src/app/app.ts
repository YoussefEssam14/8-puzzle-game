import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms'; // needed for [(ngModel)]
import { Board } from './board/board';
import { Footer } from './footer/footer';
import { PuzzleService } from './puzzle.service';
import { Algorithm, Heuristic, SolveRequest, SolveResponse } from './models';

@Component({
  selector: 'app-root',
  imports: [Board, Footer, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private service = inject(PuzzleService);

  // The board is 9 numbers. 0 is the empty gap.
  board = signal<number[]>([8,7,6,0,4,1,2,5,3]);

  // The message box (the type is a Bootstrap color: primary, success, danger...)
  message = signal('Click a tile next to the gap.');
  messageType = signal('secondary');

  busy = signal(false); // true while loading or playing a solution
  loading = signal(false); // true only while waiting for the backend to solve

  // Results of the "Compare all" button (one row per algorithm)
  comparison = signal<SolveResponse[] | null>(null);
  comparing = signal(false); // true while waiting for the comparison

  // Numbers shown after a successful solve
  stats = signal<{ moves: number; expanded: number; time: number; search_depth: number } | null>(null);

  // Solution path explorer
  solutionPath = signal<number[][] | null>(null);
  solutionMoves = signal<string[]>([]);
  pathStep = signal(0);

  // ----- Settings chosen by the user -----
  algorithm = signal<Algorithm>('astar');
  heuristic = signal<Heuristic>('manhattan');
  maxDepth = signal(31);
  nodeLimit = signal(5000000);
  speed = signal(2); // playback speed in moves per second

  // Custom board input (comma-separated string like "1,2,0,3,4,5,6,7,8")
  boardInput = signal('');
  boardInputError = signal('');

  // Options shown in the dropdowns
  algorithms = [
    { value: 'astar', label: 'A*' },
    { value: 'bfs', label: 'BFS' },
    { value: 'dfs', label: 'DFS' },
    { value: 'iddfs', label: 'IDDFS' },
  ];
  heuristics = ['manhattan', 'euclidean'];

  // A short explanation for each algorithm
  descriptions: Record<string, string> = {
    astar: 'A* uses a heuristic to try the most promising moves first. It finds the shortest solution.',
    bfs: 'BFS tries all moves level by level. It finds the shortest solution but uses a lot of memory.',
    dfs: 'DFS follows one path as deep as it can before going back. It is fast, but the solution can be long.',
    iddfs: 'IDDFS repeats DFS with a growing depth limit. It finds the shortest solution with little memory.',
  };

  // Small helper to change the message and its color
  private show(text: string, type: string) {
    this.message.set(text);
    this.messageType.set(type);
  }

  // Called when the Board says a tile was clicked
  onTileClick(index: number) {
    if (this.busy()) return;

    const board = [...this.board()]; // copy the list
    const gap = board.indexOf(0);

    // Row and column of the clicked tile and of the gap
    const row = Math.floor(index / 3);
    const col = index % 3;
    const gapRow = Math.floor(gap / 3);
    const gapCol = gap % 3;

    // A tile can move only if it is directly next to the gap
    const distance = Math.abs(row - gapRow) + Math.abs(col - gapCol);
    if (distance !== 1) return;

    // Swap the tile with the gap
    board[gap] = board[index];
    board[index] = 0;
    this.board.set(board);
    this.stats.set(null);
    this.comparison.set(null);
    this.solutionPath.set(null);
    this.solutionMoves.set([]);
    this.show('Keep going!', 'secondary');
  }

  // Called when the "Apply" board input button is clicked
  onApplyBoard() {
    const raw = this.boardInput().trim();
    if (!raw) {
      this.boardInputError.set('Please enter a board.');
      return;
    }

    const parts = raw.split(',').map((s) => s.trim());
    if (parts.length !== 9) {
      this.boardInputError.set('Enter exactly 9 numbers separated by commas.');
      return;
    }

    const nums = parts.map(Number);
    if (nums.some((n) => isNaN(n) || !Number.isInteger(n) || n < 0 || n > 8)) {
      this.boardInputError.set('Each number must be an integer from 0 to 8.');
      return;
    }

    const sorted = [...nums].sort((a, b) => a - b);
    const expected = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    if (sorted.some((v, i) => v !== expected[i])) {
      this.boardInputError.set('Board must contain each of 0–8 exactly once.');
      return;
    }

    this.boardInputError.set('');
    this.board.set(nums);
    this.stats.set(null);
    this.comparison.set(null);
    this.solutionPath.set(null);
    this.solutionMoves.set([]);
    this.show('Custom board applied!', 'primary');
  }

  // Called when the "New puzzle" button is clicked
  onNewPuzzle() {
    this.busy.set(true);
    this.service.random().subscribe({
      next: (data) => {
        this.board.set(data.state);
        this.stats.set(null);
        this.comparison.set(null);
        this.solutionPath.set(null);
        this.solutionMoves.set([]);
        this.show('New puzzle. Try to solve it!', 'primary');
        this.busy.set(false);
      },
      error: () => {
        this.show('Cannot reach the backend. Is it running?', 'danger');
        this.busy.set(false);
      },
    });
  }

  // Called when the "Solve" button is clicked
  onSolve() {
    // 1. Check the numbers the user typed
    const numbers = this.readNumbers();
    if (!numbers) return;
    const { depth, limit } = numbers;

    // 2. Build the request with all the settings
    const request: SolveRequest = {
      state: this.board(),
      algorithm: this.algorithm(),
      heuristic: this.heuristic(),
      max_depth: depth,
      node_limit: limit,
    };

    // 3. Send it to the backend
    this.busy.set(true);
    this.loading.set(true);
    this.stats.set(null);
    this.comparison.set(null);
    this.solutionPath.set(null);
    this.solutionMoves.set([]);
    this.show('Solving...', 'info');
    this.service.solve(request).subscribe({
      next: (result) => {
        this.loading.set(false);
        if (!result.found) {
          this.show('No solution found. ' + result.note, 'warning');
          this.busy.set(false);
          return;
        }
        this.show('Solved in ' + result.moves.length + ' moves!', 'success');
        this.stats.set({
          moves: result.moves.length,
          expanded: result.nodes_expanded,
          time: result.time_ms,
          search_depth: result.search_depth,
        });
        this.solutionPath.set(result.path);
        this.solutionMoves.set(result.moves);
        this.pathStep.set(0);
        this.playSteps(result.path);
      },
      error: () => {
        this.loading.set(false);
        this.show('Something went wrong. Is the backend running?', 'danger');
        this.busy.set(false);
      },
    });
  }

  // Called when the "Compare all" button is clicked.
  // The backend runs BFS, DFS, IDDFS and A* (both heuristics) on the current board.
  onCompare() {
    const numbers = this.readNumbers();
    if (!numbers) return;

    this.busy.set(true);
    this.comparing.set(true);
    this.stats.set(null);
    this.comparison.set(null);
    this.show('Comparing all algorithms...', 'info');

    this.service
      .compare({
        state: this.board(),
        max_depth: numbers.depth,
        node_limit: numbers.limit,
      })
      .subscribe({
        next: (results) => {
          this.comparison.set(results);
          this.show('Comparison finished.', 'success');
          this.comparing.set(false);
          this.busy.set(false);
        },
        error: (err) => {
          // The backend sends a text like "State is not solvable." when something is wrong
          const detail = err?.error?.detail;
          this.show(
            typeof detail === 'string' ? detail : 'Something went wrong. Is the backend running?',
            'danger'
          );
          this.comparing.set(false);
          this.busy.set(false);
        },
      });
  }

  // Turn "astar" into "A*" for the table
  algorithmName(value: string): string {
    return this.algorithms.find((a) => a.value === value)?.label ?? value;
  }

  // Check max depth and node limit (the backend has the same limits).
  // Returns the numbers, or null if something is wrong.
  private readNumbers(): { depth: number; limit: number } | null {
    const depth = Number(this.maxDepth());
    const limit = Number(this.nodeLimit());
    if (!(depth >= 1 && depth <= 60)) {
      this.show('Max depth must be between 1 and 60.', 'warning');
      return null;
    }
    if (!(limit >= 1000 && limit <= 20000000)) {
      this.show('Node limit must be between 1,000 and 20,000,000.', 'warning');
      return null;
    }
    return { depth, limit };
  }

  // Show the solution one board at a time.
  // We read the speed again before every step, so the slider works while playing.
  private playSteps(path: number[][]) {
    let step = 0;

    const showNext = () => {
      this.board.set(path[step]);
      step++;

      if (step >= path.length) {
        this.busy.set(false); // finished
        return;
      }

      const speed = Number(this.speed()) || 1; // moves per second
      setTimeout(showNext, 1000 / speed);
    };

    showNext();
  }

  // Convert flat board (length 9) into 3 rows of 3, used by the path explorer
  boardRows(board: number[]): number[][] {
    return [board.slice(0, 3), board.slice(3, 6), board.slice(6, 9)];
  }

  // Jump to a specific step in the path explorer
  scrollToPathStep(idx: number) {
    this.pathStep.set(idx);
    const el = document.getElementById(`path-step-${idx}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
}