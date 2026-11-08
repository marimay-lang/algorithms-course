# Scans, prefix sums and windows

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/05-sequences
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/sequences/).

## Invariant

prefix[k] equals the sum of the first k input values. The sliding-window deque has increasing indices and decreasing values; its front is the maximum remaining candidate.

## Trace

For [4,-2,7,-1], prefix sums are [0,4,2,9,8]. The sum of [1,3) is 9-4=5. For [1,3,-1,-3,5] and width 3 the window maxima are [3,3,5].

## Cost

Min/max, reversal, rotation, prefix construction and sorted deduplication are O(n). Range queries are O(1) after preprocessing. Sliding maximum is O(n): every index enters and leaves at most once. Prefix/dedup output is O(n); the deque implementation also retains O(n) slots. Reversal and rotation use O(1) auxiliary space.

## Contract

Range endpoints are half-open. rangeSum accepts a prefix array produced by prefixSums. Negative rotations, invalid windows, unsorted dedup input and overflowing sums are explicitly rejected. Empty min/max has no result.

## Exercise

Replace the retained deque storage with a ring buffer, preserving the monotone invariant. Add an oracle test for every window width.
