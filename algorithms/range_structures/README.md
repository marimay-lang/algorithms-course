# Range structures

All indices are zero-based and every query interval is half-open `[start, end)`.
Constructors take a snapshot of integer input values. Record aliases refer to
the same structure, so a successful update through an alias is visible through
the original handle. Fields stay private to the package.

| Structure and API | Construction / storage | Operation time | Extra operation space |
| --- | --- | --- | --- |
| `newFenwick`, `FenwickTree` | O(n log n) / O(n) | `add`, `prefixSum`: O(log n) | Update O(log n); query O(1) |
| `newSegmentTree`, `SegmentTree` | O(n) / O(n) | `set`, `rangeSum`: O(log n) | Update O(log n); query O(1) |
| `newSparseTable`, `SparseTable` | O(n log n) / O(n log n) | `minimum`: O(1) | O(1) |

`newFenwick(values)`, `newSegmentTree(values)`, and `newSparseTable(values)`
return `Result<Structure, Error>`. Each type owns an ordinary public
`length(structure): int` function, also available through dot-call syntax.
The remaining signatures are:

```marimay
public fn add(tree: FenwickTree, index: int, delta: int): Result<void, Error>;
public fn prefixSum(tree: FenwickTree, end: int): Result<int, Error>;
public fn set(tree: SegmentTree, index: int, value: int): Result<void, Error>;
public fn rangeSum(tree: SegmentTree, start: int, end: int): Result<int, Error>;
public fn minimum(table: SparseTable, start: int, end: int): Result<int, Error>;
```

Fenwick stores a point-value snapshot as well as partial sums, so a point
overflow cannot hide behind cancellation in an aggregate. Both mutable
structures stage O(log n) affected values before committing; an overflow
leaves every point and aggregate unchanged. They do not copy or rebuild the
whole structure on each update. Constructors and queries also check every
intermediate sum. A failed construction publishes no partially built handle.

Empty structures are valid. Empty sums are zero; an empty minimum reports
`Error.EmptyRange`. An out-of-bounds index reports `InvalidIndex`; negative,
reversed, and past-end intervals report `InvalidRange`. An empty interval is
checked for bounds before minimum reports `EmptyRange`. Unrepresentable sums
and point updates report `ArithmeticOverflow`; impossible storage-size
arithmetic reports `SizeOverflow`. Runtime heap limits remain execution
failures rather than additional source error cases.

The sparse table is static. It stores copied power-of-two range minima and
uses two overlapping blocks for a query. For tiny arrays, construction has a
constant floor; the asymptotic table describes growing nonempty inputs.

Tests compare every interval to direct summation/minimum scans, repeat point
updates against a plain-array model, verify input ownership and alias identity,
exercise empty/invalid intervals, and check that both early and later overflow
failures leave the original structure intact.
