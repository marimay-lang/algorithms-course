# Exchange arguments and reachable frontiers

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/12-greedy
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/greedy/).

## Invariant

Choosing the earliest finishing compatible interval leaves at least as much room as any other first choice. Each minimum-jumps boundary contains exactly the positions reachable using the current number of jumps. Optimal merging combines the two smallest available weights.

## Trace

The positive-length intervals [1,3), [2,5), [3,4) admit [1,3), [3,4). Weights [1,2,3,4] merge with costs 3+6+10=19. Jump limits [2,3,1,1,4] need two jumps.

## Cost

Interval selection and union use insertion sorting: O(n^2) time and O(n) storage. Minimum jumps is O(n) time and O(1) space. Optimal merging is O(n log n) time and O(n) heap storage.

## Contract

Selection uses positive-length half-open intervals and permits touching. Union uses closed intervals and merges touching endpoints; zero-length closed intervals are valid. Inputs are not reordered. Jump limits and merge weights must be nonnegative; unreachable jumps or overflow return None. An empty jump sequence needs zero jumps.

## Exercise

Give a counterexample to choosing the shortest interval first. Then replace insertion sorting with an iterative O(n log n) sort while retaining the same tie and endpoint rules.
