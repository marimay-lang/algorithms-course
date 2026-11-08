# Lesson 1: cost model and a linear scan

## Model

Input size `n` is the number of array elements. `O(1)` means the number of
significant operations is bounded by a constant independent of `n`; `O(n)`
means the upper bound grows no faster than a linear function of `n`.

In `countAbove`, after processing the first `k` elements, `count` equals the
number of elements in `values[0..k)` strictly greater than `threshold`.
This is the loop invariant.

The array values have no preconditions. The postcondition is that the result
equals the number of all input elements strictly above the threshold.
The algorithm reads every element once: O(n) time and O(1) auxiliary memory.
The input itself is excluded from auxiliary-memory accounting.

In the bounded preview used for this lesson, tests use `@test` and explicit
checks with `panic`. The target contract describes `expect.equal`, but the
installed checker did not yet permit that entire API.

## Manual trace

For `[4, -1, 7, 7, 2]` and threshold `3`:

| Processed element | Processed prefix | `count` |
|---:|---|---:|
| — | `[]` | 0 |
| 4 | `[4]` | 1 |
| -1 | `[4, -1]` | 1 |
| 7 | `[4, -1, 7]` | 2 |
| 7 | `[4, -1, 7, 7]` | 3 |
| 2 | `[4, -1, 7, 7, 2]` | 3 |

Initialization gives the correct count for an empty prefix. Each iteration
preserves the invariant by incrementing exactly for a qualifying element.
At termination the entire array has been processed, turning the invariant
into the postcondition.
