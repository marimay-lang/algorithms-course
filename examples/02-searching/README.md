# Search and half-open boundaries

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/02-searching
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/searching/).

## Invariant

A binary bound maintains that every position before low fails the boundary predicate and every position at or after high satisfies it. The unclassified interval shrinks on each comparison.

## Trace

For [1,2,2,2,5], lowerBound(2)=1 and upperBound(2)=4. An absent 3 has insertion position 4; its binary search returns None.

## Cost

Linear and last-occurrence search take O(n) time. Binary search and bounds take O(log n). Jump search takes O(sqrt n); exponential search takes O(log p) for a nearby answer at position p, bounded by O(log n). All use O(1) auxiliary memory.

## Contract

Ordered search requires ascending input. It does not spend O(n) validating that precondition. Bounds return an insertion position in [0,n]; first/last occurrence search returns None when absent.

## Exercise

Derive equalRange from two bounds and count duplicates. Add tests for absent targets before, between and after stored values.
