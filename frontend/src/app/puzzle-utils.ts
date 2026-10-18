export function tryMove(state: number[], i: number, size: number): number[] | null {
  const blank = state.indexOf(0);
  const sameRow = Math.floor(i / size) === Math.floor(blank / size);
  const sameCol = i % size === blank % size;
  const adjacent =
    (sameRow && Math.abs(i - blank) === 1) ||
    (sameCol && Math.abs(i - blank) === size);
  if (!adjacent) return null;

  const next = [...state];
  [next[i], next[blank]] = [next[blank], next[i]];
  return next;
}