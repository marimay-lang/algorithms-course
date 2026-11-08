# States, recurrences and update order

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/10-dynamic-programming
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/dynamic/).

## Invariant

Each table entry summarizes an explicitly defined smaller problem. Ascending amounts permit unlimited coin reuse; descending capacities ensure a 0/1 item or subset element is used at most once. Rolling rows retain only the dependency frontier.

## Trace

For coins [1,3,4] and amount 6, greedy 4+1+1 uses three coins, while the DP finds 3+3 using two. This separates a proved recurrence from a tempting local choice.

## Cost

Coin routines first validate distinct positive denominations with pairwise comparisons: their full time is O(coinCount^2 + (amount+1)*coinCount), with O(amount+1) table space. Knapsack/subset sum are pseudo-polynomial in capacity/target. LIS is O(n^2); LCS and edit distance use O(mn+m+n) time including empty-axis initialization, with a rolling row. Fibonacci and Kadane are O(n) time, O(1) space.

## Contract

Coin denominations must be positive and distinct. Knapsack weights/capacity and subset-sum values/target are nonnegative; knapsack values may be negative and zero-weight items are used once. Maximum subarray is nonempty. None reports documented invalid, unreachable, overflow or table-growth cases; inspect each signature.

## Exercise

Reconstruct a chosen coin combination, then a chosen knapsack item set. State which tie you choose and test it. Contrast unordered coin combinations with ordered sequences.
