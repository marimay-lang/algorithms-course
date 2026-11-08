# Data structures

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/04-data-structures
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/structures/).

## Invariant

The stack owns a LIFO suffix, the queue consumes a FIFO prefix, and each heap parent is no greater than its children. DSU parent links form a forest whose roots identify connected sets.

## Trace

After pushing 7, 2, 9, 1 into the heap, successive removals return 1, 2, 7, 9. Joining (0,1) and (1,2) connects 0 to 2 without connecting 3.

## Cost

Stack push is amortized O(1); pop is O(1). Queue enqueue is amortized O(1), dequeue O(1); consumed slots are retained, so storage tracks total enqueues. Heap push/pop cost O(log n), minimum O(1). DSU uses path compression and union by rank: amortized O(alpha(n)) per operation and O(n) storage.

## Contract

DSU requires a nonnegative size and valid indices. tryNewDsu returns None for a negative size; newDsu asserts the constructor precondition. Empty stack/queue/heap removal returns None. Arrays/fields are shared mutable references; use constructors and package functions.

## Exercise

Implement queue compaction when the consumed prefix becomes large. Explain how to preserve FIFO order and measure retained storage.
