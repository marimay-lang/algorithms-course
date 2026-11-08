# Counting, sets and cancellation

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/06-hashing
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/hashing/).

## Invariant

Before twoSum examines index i, the map contains earlier values and their first indices. Multiset intersection consumes exactly one available occurrence. Boyer-Moore cancellation only proposes a candidate, so a second pass verifies it.

## Trace

stableUnique([4,2,4,1,2]) returns [4,2,1]. Intersecting [3,2,3,1,3] with [3,3,4,2] returns [3,2,3], retaining multiplicity and left-input order.

## Cost

Hash-based scans take expected O(n+m) time and O(distinct keys) storage, plus their output. twoSum and stableUnique are expected O(n). Majority vote is deterministic O(n) time and O(1) space. See [counting](../../algorithms/counting) for integer and Unicode frequency maps.

## Contract

twoSum returns distinct indices, with no promise of a lexicographically smallest pair. Overflowing complements are skipped. majority returns None unless a value occurs strictly more than n/2 times. Rune frequencies count Unicode scalars.

## Exercise

Implement an anagram predicate using rune frequency maps. Test repeated scalars, empty inputs and a combining-mark example; explain why normalization is a separate contract.
