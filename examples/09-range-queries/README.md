# Preprocessing and mutable range structures

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/09-range-queries
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/range_structures/).

## Invariant

Fenwick nodes own suffix blocks determined by their least significant set bit. Segment-tree parents summarize two disjoint child ranges. Sparse-table entries summarize power-of-two intervals of a static array.

## Trace

Starting with [2,1,3,4], the prefix of length 3 is 6. Update index 1 by +5 and the prefix becomes 11. A half-open sum [1,4) is then 13.

## Cost

Fenwick prefix queries and point additions are O(log n). Segment-tree range sums and point replacement are O(log n). Sparse-table preprocessing uses O(n log n) time/space; a static range minimum query is O(1). Fenwick construction here is O(n log n); segment-tree construction is O(n). Both mutable trees occupy O(n) storage, and failure-atomic updates temporarily stage O(log n) cells before committing them.

## Contract

Indices and intervals are validated; range sums use half-open endpoints. Updates preflight affected sums so an arithmetic error does not leave a partially changed tree. Sparse tables are immutable after construction. Empty minimum ranges have no minimum.

## Exercise

Add an independent plain-array model and run alternating updates and range queries. After a rejected overflow update, verify every observable range is unchanged.
