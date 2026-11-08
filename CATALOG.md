# Implemented algorithm catalogue

This is a finite syllabus for the MIT-licensed Marimay personal learning project.
It contains **83 library entries: 82 implementation/data-structure entries and
one directed-cycle convenience query**. The count describes documented library
entries, not 83 independent mathematical ideas or every possible algorithm.
Constructors, accessors, operation helpers, `tryNewDsu`, and private exercise/demo
functions are not counted again. A structure and its operations occupy one row.
The separate `bfsPath` row describes the implemented path-producing BFS variant.

Every API below is declared in the linked source. Imports use
`course.local/algorithms/algorithms/<package>`; functions are ordinary top-level
functions, with dot-call syntax where the language permits it. See the
[course README](README.md) for the twelve lessons and verification commands.
Focused tests sit beside their source in `_test.my` files.

## Reading the costs and contracts

Time describes the actual implementation, including its validation. Bounds are
worst-case unless marked average, expected or amortized. Constant floors for
empty/tiny inputs are implicit. **Extra space excludes the input and includes
returned arrays/maps unless a row separates working space and result storage.**
For persistent structures, stored representation and temporary operation space
are stated separately. Costs are algorithmic storage, without a promise about
GC timing, allocator overhead or process RSS.

Marimay `int` is signed i64 and ordinary overflow traps. The documented
Option/Result outcomes cover each API's validated source conditions; they do
not turn heap-budget exhaustion or host allocation failure into recoverable
values. Sorted-input and DSU-index preconditions must be respected. Shared
array/record references observe in-place mutation. Implementations use loops
and explicit worklists because the current native emitter rejects recursion.

| Group | Entries |
| --- | ---: |
| [Searching](#searching) | 7 |
| [Sorting](#sorting) | 13 |
| [Basic data structures](#basic-data-structures) | 4 |
| [Sequence scans and windows](#sequence-scans-and-windows) | 7 |
| [Hashing and counting](#hashing-and-counting) | 7 |
| [Integer mathematics](#integer-mathematics) | 9 |
| [Graph algorithms](#graph-algorithms) | 14 |
| [Range-query data structures](#range-query-data-structures) | 3 |
| [Dynamic programming](#dynamic-programming) | 9 |
| [Unicode scalar algorithms](#unicode-scalar-algorithms) | 6 |
| [Greedy algorithms](#greedy-algorithms) | 4 |
| **Total** | **83** |

## Searching

n is array length. Ordered APIs require nondecreasing input; they do not spend O(n) verifying this precondition. First/last matching indices are zero-based; bounds may return n.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 1 | [`searching.linearSearch`](algorithms/searching/linear.my#L1) | O(n) | O(1) | First matching index, or None; unsorted inputs are allowed; no mutation. |
| 2 | [`searching.lastIndexOf`](algorithms/searching/linear.my#L10) | O(n) | O(1) | Last matching index, or None; unsorted inputs are allowed; no mutation. |
| 3 | [`searching.binarySearch`](algorithms/searching/binary.my#L2) | O(log n) | O(1) | Nondecreasing input is a caller precondition; returns the first duplicate match or None. |
| 4 | [`searching.lowerBound`](algorithms/searching/binary.my#L20) | O(log n) | O(1) | Nondecreasing input; first index with value >= target, or n. |
| 5 | [`searching.upperBound`](algorithms/searching/binary.my#L34) | O(log n) | O(1) | Nondecreasing input; first index with value > target, or n. |
| 6 | [`searching.jumpSearch`](algorithms/searching/jump.my#L2) | O(sqrt(n)) | O(1) | Nondecreasing input; first match; computes an integer stride without a math-library dependency. |
| 7 | [`searching.exponentialSearch`](algorithms/searching/binary.my#L48) | O(log(p+1)), worst O(log(n+1)) | O(1) | Nondecreasing input; first match near position p; bound doubling is guarded. |

## Sorting

All comparison sorts accept full signed-i64 keys. Mutation is visible through array aliases. Returned-array distribution sorts leave their input unchanged. Stability on equal bare integers does not establish a tagged-record stability contract.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 8 | [`sorting.selectionSort`](algorithms/sorting/comparison.my#L7) | O(n^2) | O(1) | Mutates the integer array in place; full signed-i64 key domain. |
| 9 | [`sorting.bubbleSort`](algorithms/sorting/comparison.my#L21) | O(n^2), best O(n) | O(1) | In-place adjacent swaps with an early exit when no swap occurs. |
| 10 | [`sorting.cocktailSort`](algorithms/sorting/comparison.my#L38) | O(n^2), best O(n) | O(1) | In-place bidirectional adjacent-swap passes. |
| 11 | [`sorting.gnomeSort`](algorithms/sorting/comparison.my#L69) | O(n^2), best O(n) | O(1) | In-place backward/forward adjacent corrections. |
| 12 | [`sorting.insertionSort`](algorithms/sorting/insertion.my#L1) | O(n^2), best O(n) | O(1) | In-place insertion into a sorted prefix. |
| 13 | [`sorting.combSort`](algorithms/sorting/comparison.my#L81) | O(n^2) worst | O(1) | In-place; this implementation shrinks gaps by 10/13 with overflow-safe arithmetic. |
| 14 | [`sorting.shellSort`](algorithms/sorting/comparison.my#L105) | O(n^2) worst | O(1) | In-place; the bound applies to this implementation's halving-gap schedule. |
| 15 | [`sorting.mergeSort`](algorithms/sorting/merge.my#L28) | O(n log n) | O(n) | Mutates the result in place using one copied workspace and iterative bottom-up merges. |
| 16 | [`sorting.heapSort`](algorithms/sorting/heap.my#L20) | O(n log n) | O(1) | In-place max-heap construction followed by repeated extraction. |
| 17 | [`sorting.quickSort`](algorithms/sorting/quick.my#L8) | O(n log n) average; O(n^2) worst | O(log n) | Iterative three-way partitioning; process the smaller side immediately. Returns Result<void,ArrayGrowthError>; no general rollback promise after partial mutation. |
| 18 | [`sorting.countingSort`](algorithms/sorting/distribution.my#L3) | O(n+k), k=maximumKey+1 | O(n+k) | Returns a new sorted array. Keys must be in [0,maximumKey]; negative/max-i64 bounds, invalid keys or logical growth rejection return None. |
| 19 | [`sorting.bucketSort`](algorithms/sorting/distribution.my#L43) | O(n+b+sum(bucketSize^2)); worst O(n^2+b) | O(n+b) | Returns a new array; positive width/count, nonnegative keys and key/width < count. Uses insertion sort inside each bucket; invalid domain/growth returns None. |
| 20 | [`sorting.radixSort`](algorithms/sorting/radix.my#L11) | O(8*(n+256)) | O(n+256) | Full signed-i64 domain; eight stable byte passes with a final sign-bit transform. Mutates input; logical workspace growth is returned as Result. |

## Basic data structures

One entry groups a nominal structure with its constructors and operations. The functions remain ordinary package functions with eligible dot calls; methods do not add catalogue entries. n is live heap size, h is the maximum size reached by that stack/heap, and q is total enqueues. Array removals retain reserved storage.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 21 | [`structures.Stack; newStack, push, pop, top, length, empty`](algorithms/structures/stack.my#L1) | push amortized O(1); pop/top/length/empty O(1) | O(h) retained; O(1) operation work | Use newStack, push, pop, top, length, empty. Empty pop/top returns None. Mutating operations share the same handle. |
| 22 | [`structures.Queue; newQueue, enqueue, dequeue, front, length, empty`](algorithms/structures/queue.my#L1) | enqueue amortized O(1); dequeue/front/length/empty O(1) | O(q) stored; O(1) operation work | Use newQueue/enqueue/dequeue/front. q is total enqueues, because consumed slots are retained; empty access returns None. |
| 23 | [`structures.MinHeap; newMinHeap, push, pop, minimum, length, empty`](algorithms/structures/heap.my#L1) | push/pop O(log n); minimum/length/empty O(1) | O(h) retained; O(1) operation work | Use newMinHeap and ordinary package operations. Duplicate/negative keys are valid; empty pop/minimum returns None. |
| 24 | [`structures.Dsu; newDsu, tryNewDsu, find, union, connected, components`](algorithms/structures/dsu.my#L1) | construction O(n); find/union amortized O(alpha(n)) | O(n) stored; O(1) operation work | Path compression and union by rank. tryNewDsu rejects negative size; newDsu requires nonnegative size and operations require valid indices. connected shares find's cost; components is O(1). |

## Sequence scans and windows

All intervals are half-open. d is distinct output count. In-place reverse/rotate intentionally use index-based loops; prefix, deduplication and window results are new arrays.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 25 | [`sequences.minMax`](algorithms/sequences/sequences.my#L1) | O(n) | O(1) | Returns Some((minimum,maximum)); an empty input returns None. |
| 26 | [`sequences.reverse`](algorithms/sequences/sequences.my#L30) | O(n) | O(1) | Reverses the shared array in place; empty input is valid. |
| 27 | [`sequences.rotateLeft`](algorithms/sequences/sequences.my#L35) | O(n) | O(1) | In-place three-reversal rotation; count is reduced modulo length. A negative count returns false without mutation; empty nonnegative rotation succeeds. |
| 28 | [`sequences.prefixSums`](algorithms/sequences/sequences.my#L49) | O(n) | O(n) result | Returns a new [0,...] prefix array. Every prefix sum must fit i64; overflow returns None. |
| 29 | [`sequences.rangeSum`](algorithms/sequences/sequences.my#L65) | O(1) | O(1) | Half-open [start,end) over a prefixSums result. Invalid bounds or overflowing subtraction return None; an empty valid range sums to zero. |
| 30 | [`sequences.deduplicateSorted`](algorithms/sequences/sequences.my#L72) | O(n) | O(d) result | Nondecreasing integers produce a new array of d distinct values. Unsorted input returns None; the source is unchanged. |
| 31 | [`sequences.slidingMaximum`](algorithms/sequences/sequences.my#L86) | O(n) | O(n) deque plus O(n-w+1) result | Monotone index deque; width w must satisfy 1 <= w <= n. Stale prefix slots are retained, so auxiliary storage is O(n), not O(w). |

## Hashing and counting

n/m are input lengths and d is distinct-key count. Hash-table bounds are expected, not collision-independent worst-case guarantees. Counting maps retain first insertion order.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 32 | [`hashing.stableUnique`](algorithms/hashing/hashing.my#L2) | O(n) expected | O(d) set plus O(d) result | Preserves the first encounter of each integer; input is unchanged. |
| 33 | [`hashing.twoSum`](algorithms/hashing/hashing.my#L15) | O(n) expected | O(d) | Returns distinct indices or None. Unrepresentable complements are skipped; no lexicographically smallest-pair promise. |
| 34 | [`hashing.multisetIntersection`](algorithms/hashing/hashing.my#L32) | O(n+m) expected | O(d_right) map plus O(result size) | Consumes right-side multiplicities while preserving left encounter order in a new array. |
| 35 | [`hashing.majority`](algorithms/hashing/hashing.my#L56) | O(n) | O(1) | Boyer-Moore candidate selection followed by verification; returns None unless a value occurs strictly more than n/2 times. |
| 36 | [`counting.intFrequencies`](algorithms/counting/counting.my#L1) | O(n) expected | O(d) result | Integer-key frequency map; values are counts and iteration retains first key insertion order. |
| 37 | [`counting.uniqueIntCount`](algorithms/counting/counting.my#L13) | O(n) expected | O(d) | Returns the number of distinct integers using a set. |
| 38 | [`counting.runeFrequencies`](algorithms/counting/counting.my#L21) | O(n) expected | O(d) result | Counts explicit Unicode scalars in []rune, without normalization or grapheme grouping. |

## Integer mathematics

Integer arithmetic has fixed i64 semantics. These costs use unit-cost fixed-width arithmetic; they are not arbitrary-precision complexity claims. Parameter/domain checks precede unsafe arithmetic.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 39 | [`numeric.gcd`](algorithms/numeric/number_theory.my#L2) | O(log(min(a,b)+1)) for positive inputs; zero cases O(1) | O(1) | Nonnegative inputs; gcd(0,0)=0. Negative input returns None. |
| 40 | [`numeric.lcm`](algorithms/numeric/number_theory.my#L16) | GCD cost plus O(1) | O(1) | Nonnegative inputs; lcm(0,x)=0. Division before checked multiplication avoids unnecessary product overflow; None for invalid/overflow. |
| 41 | [`numeric.power`](algorithms/numeric/number_theory.my#L32) | O(log(exponent+1)) | O(1) | Signed base and nonnegative exponent; 0^0=1. Checked exponentiation by squaring returns None for an unrepresentable result. |
| 42 | [`numeric.modularPower`](algorithms/numeric/number_theory.my#L85) | O(log(exponent+1)*log(modulus+1)) | O(1) | Nonnegative base/exponent and positive modulus. Repeated doubling uses overflow-safe modular addition; modulus one returns zero. |
| 43 | [`numeric.isPrime`](algorithms/numeric/number_theory.my#L104) | O(sqrt(value)) worst | O(1) | Values below two are false. Trial divisors use divisor <= value/divisor rather than an overflowing square. |
| 44 | [`numeric.sieve`](algorithms/numeric/number_theory.my#L122) | O(limit*log log limit) | O(limit) flags plus prime-list result | Returns primes strictly below a nonnegative limit. Negative limits return None; tiny limits use constant-sized work. |
| 45 | [`numeric.primeFactors`](algorithms/numeric/number_theory.my#L153) | O(sqrt(value)) worst | O(log(value)) result; O(1) work | Input must be >=1. Returns repeated prime factors in ascending order; one has an empty factorization; invalid input returns None. |
| 46 | [`numeric.binomial`](algorithms/numeric/number_theory.my#L173) | O(n*w), w=min(k,n-k)>0; O(1) for w=0 | O(w+1) | Requires 0 <= k <= n. Rolling Pascal row with checked addition; None for invalid input or overflow. |
| 47 | [`numeric.integerSquareRoot`](algorithms/numeric/number_theory.my#L208) | O(log(value+1)) | O(1) | Returns floor(sqrt(value)); negative input returns None. Comparison by division avoids squaring overflow. |

## Graph algorithms

V is vertex count; E counts stored directed adjacency entries, including both directions of an undirected edge. U is the extra reverse-edge validation scan: O(sum over stored (u,v) of (degree(u)+degree(v))), bounded by O(E*Delta), and O(E^2) for a multigraph. Each call also scans all rows/endpoints, including unreachable components. Undirected entries include U in their full-call time. All APIs return Result<value,Error>; optional distances reserve no integer sentinel. Every attempted intermediate path/tree sum is checked, so ArithmeticOverflow may precede a later cycle or alternative-path outcome. Empty whole-graph queries are valid; source-based traversals require a valid start.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 48 | [`graph_algorithms.dfs`](algorithms/graph_algorithms/traversal.my#L2) | O(V+E) | O(V) | Directed adjacency lists; discovery order from a valid start follows neighbor order. Validates every endpoint. |
| 49 | [`graph_algorithms.bfsDistances`](algorithms/graph_algorithms/traversal.my#L33) | O(V+E) | O(V) | Unweighted hop distances as []Option<int>; unreachable vertices are None. |
| 50 | [`graph_algorithms.bfsPath`](algorithms/graph_algorithms/traversal.my#L60) | O(V+E) | O(V) | Result<Option<[]int>,Error>; a shortest-hop path includes both endpoints, and an unreachable target is Ok(None). |
| 51 | [`graph_algorithms.connectedComponents`](algorithms/graph_algorithms/traversal.my#L99) | O(V+E+U) | O(V) | Labels an exactly symmetric undirected multigraph, including parallel-edge multiplicities; empty graph returns empty labels. |
| 52 | [`graph_algorithms.topologicalOrder`](algorithms/graph_algorithms/traversal.my#L125) | O(V+E) | O(V) | Kahn ordering of the entire directed graph; any cycle returns Error.Cycle. |
| 53 | [`graph_algorithms.hasDirectedCycle (query wrapper)`](algorithms/graph_algorithms/traversal.my#L157) | O(V+E) | O(V) | Convenience query over topologicalOrder: Cycle becomes true, while malformed input remains an error. Counted as a query entry, not an additional implementation. |
| 54 | [`graph_algorithms.bipartiteColoring`](algorithms/graph_algorithms/traversal.my#L165) | O(V+E+U) | O(V) | Exactly symmetric undirected input; colors 0/1 in every component. A self-loop or odd cycle returns NotBipartite. |
| 55 | [`graph_algorithms.stronglyConnectedComponents`](algorithms/graph_algorithms/traversal.my#L192) | O(V+E) | O(V+E) | Iterative Kosaraju with a copied reverse graph; returns component labels. |
| 56 | [`graph_algorithms.dagShortestPaths`](algorithms/graph_algorithms/paths.my#L2) | O(V+E) | O(V+E) | Signed weights are allowed; the entire graph must be acyclic. Returns optional distances; copies unweighted adjacency for topological processing. |
| 57 | [`graph_algorithms.bellmanFord`](algorithms/graph_algorithms/paths.my#L29) | O(V*(V+E)) | O(V) | Signed weights; rejects negative cycles reachable from the start. Full vertex scans on each pass are included in the bound. |
| 58 | [`graph_algorithms.dijkstra`](algorithms/graph_algorithms/paths.my#L79) | O(V^2+E) | O(V) | Dense selection scan; rejects every negative edge, including unreachable ones. Unreachable distances remain None. |
| 59 | [`graph_algorithms.floydWarshall`](algorithms/graph_algorithms/paths.my#L136) | O(V^3+E) | O(V^2) result matrix | All-pairs optional distances; keeps the lightest parallel edge and rejects a negative cycle anywhere. |
| 60 | [`graph_algorithms.prim`](algorithms/graph_algorithms/spanning.my#L9) | O(V^2+E+U) | O(V) | Dense Prim on a symmetric weighted multigraph; negative weights allowed. Empty tree has weight zero; a nonempty disconnected graph returns Disconnected. |
| 61 | [`graph_algorithms.kruskal`](algorithms/graph_algorithms/spanning.my#L88) | O(V+E^2+U) | O(V+E) | Symmetric weighted input; insertion-sorts candidate edges before DSU. Negative weights allowed; disconnected nonempty input is an error. |

## Range-query data structures

All constructors return Result<Structure,Error>, own integer snapshots, and allow empty input. Handles alias the same stored structure. Mutable updates are failure-atomic after staging O(log n) cells; queries/constructors check intermediate sums. InvalidIndex, InvalidRange, EmptyRange, ArithmeticOverflow and SizeOverflow remain distinct. Runtime heap failure is an execution outcome.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 62 | [`range_structures.FenwickTree; newFenwick, add, prefixSum, length`](algorithms/range_structures/fenwick.my#L1) | build O(n log n); add/prefixSum O(log n) | O(n) stored; update O(log n) scratch, query O(1) | newFenwick snapshots point values and partial sums. add(index,delta) stages all changes, including the point value; prefixSum(end) sums [0,end). Empty valid prefix is zero. |
| 63 | [`range_structures.SegmentTree; newSegmentTree, set, rangeSum, length`](algorithms/range_structures/segment.my#L1) | build O(n); set/rangeSum O(log n) | O(n) stored; update O(log n) scratch, query O(1) | newSegmentTree owns a snapshot; set replaces one point after preflighting every ancestor. rangeSum uses [start,end); an empty valid range sums to zero. |
| 64 | [`range_structures.SparseTable; newSparseTable, minimum, length`](algorithms/range_structures/sparse.my#L1) | build O(n log n); minimum O(1) | O(n log n) stored; query O(1) scratch | newSparseTable snapshots static values. minimum queries [start,end); valid empty ranges return EmptyRange, and invalid bounds are rejected first. No update API. |

## Dynamic programming

Amounts/capacities/targets give pseudo-polynomial bounds. Coin inputs are validated for distinctness by pairwise comparisons, adding O(coinCount^2) before the table recurrence. Table-size/logical-growth failures and documented invalid/overflow cases return None; resource limits retain runtime classification. In two-sequence rows, m/n are left/right lengths. Length counters are bounded by existing input sizes.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 65 | [`dynamic.fibonacci`](algorithms/dynamic/counting.my#L3) | O(index), stopping at overflow | O(1) | F(0)=0,F(1)=1. Negative indices or i64 overflow return None; F(92) is the last representable term. |
| 66 | [`dynamic.minimumCoins`](algorithms/dynamic/counting.my#L29) | O(C^2+A*C+A), A=amount, C=coinCount | O(amount) | Unlimited positive distinct denominations; None for invalid input, unreachable amount or unrepresentable table size. |
| 67 | [`dynamic.countCoinCombinations`](algorithms/dynamic/counting.my#L65) | O(C^2+A*C+A), A=amount, C=coinCount | O(amount) | Unordered unlimited-coin combinations; zero amount has one empty combination. Positive distinct denominations; None for invalid input, size or any intermediate count overflow. |
| 68 | [`dynamic.knapsack01`](algorithms/dynamic/subsets.my#L5) | O(N*C+N+C), N=itemCount, C=capacity | O(capacity) | Nonnegative weights/capacity, possibly negative values; empty selection allowed, zero-weight items used once. None for invalid lengths/domain or arithmetic overflow. |
| 69 | [`dynamic.longestIncreasingSubsequenceLength`](algorithms/dynamic/sequences.my#L2) | O(n^2) | O(n) | Strictly increasing subsequence; empty input returns Some(0). |
| 70 | [`dynamic.longestCommonSubsequenceLength`](algorithms/dynamic/sequences.my#L25) | O(m*n+m+n) | O(n) | Integer sequences, preserving order rather than contiguity; empty input yields zero. One rolling row. |
| 71 | [`dynamic.levenshteinDistance`](algorithms/dynamic/sequences.my#L55) | O(m*n+m+n) | O(n) | []rune sequences with unit insertion/deletion/substitution cost; counts Unicode scalars, and does not treat transposition as one edit. |
| 72 | [`dynamic.maximumSubarray`](algorithms/dynamic/sequences.my#L113) | O(n) | O(1) | Nonempty contiguous subarray; empty input or an unrepresentable maximum returns None. Negative prefixes reset without irrelevant underflow. |
| 73 | [`dynamic.subsetSum`](algorithms/dynamic/subsets.my#L50) | O(N*T+N+T), N=itemCount, T=target | O(target) | Nonnegative values/target; each input can be selected once, including zero. None for invalid input or unrepresentable target+1 table size. |

## Unicode scalar algorithms

For searching, n is text length and m is pattern length. Inputs are []rune, typically obtained from std/text.runes(text, explicitLimit). Offsets, spans and run counts measure Unicode scalars, not UTF-8 bytes or graphemes. No normalization or case folding is applied. Returned Option values also report documented logical-growth failures.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 74 | [`text_algorithms.findNaive`](algorithms/text_algorithms/search.my#L3) | O(n*m) | O(1) | First scalar-array match; empty pattern matches at zero, absence returns None. |
| 75 | [`text_algorithms.findKmp`](algorithms/text_algorithms/search.my#L57) | O(n+m) | O(m) | Same first-match/empty-pattern contract, using a prefix table. No raw string indexing. |
| 76 | [`text_algorithms.zValues`](algorithms/text_algorithms/search.my#L84) | O(n) | O(n) result | Z prefix-match lengths; z[0]=0. Logical result-growth failure is None. |
| 77 | [`text_algorithms.longestPalindrome`](algorithms/text_algorithms/spans.my#L10) | O(n^2) | O(1) | Odd/even center expansion; RuneSpan(start,length), earliest start on equal lengths. Empty span is (0,0). |
| 78 | [`text_algorithms.runLengthEncode`](algorithms/text_algorithms/runs.my#L8) | O(n) | O(runCount) result | Consecutive RuneRun(value,count) records retain scalar values and positive counts. Empty input produces an empty result. |
| 79 | [`text_algorithms.longestDistinctSubstring`](algorithms/text_algorithms/spans.my#L33) | O(n) expected | O(distinct scalars) | Last-position map and sliding window; returns earliest longest all-distinct RuneSpan, including (0,0) for empty input. |

## Greedy algorithms

Interval and merge-weight input domains are part of each proof. Selection uses half-open intervals, while union uses closed intervals; these contracts deliberately differ. Interval arrays are copied before sorting.

| # | Entry / API | Time | Extra space | Contract |
| ---: | --- | --- | --- | --- |
| 80 | [`greedy.intervalSchedule`](algorithms/greedy/greedy.my#L41) | O(n^2) | O(n) | Insertion sort by end time, then maximum-cardinality selection of positive-length half-open intervals. Touching is allowed; invalid/reversed/zero-length input returns None. |
| 81 | [`greedy.mergeIntervals`](algorithms/greedy/greedy.my#L69) | O(n^2) | O(n) | Insertion sort by start, then union of closed intervals; touching endpoints merge and zero-length closed intervals are valid. Input order is unchanged. |
| 82 | [`greedy.minimumJumps`](algorithms/greedy/greedy.my#L93) | O(n) | O(1) | Nonnegative maximum-forward-jump limits; empty/singleton input needs zero jumps. None means invalid input or unreachable final index; reach arithmetic is bounded. |
| 83 | [`greedy.optimalMergeCost`](algorithms/greedy/greedy.my#L132) | O(n log n) | O(n) | Repeatedly merge two minimum nonnegative weights. Empty/singleton cost is zero; negative weights or intermediate merged/total overflow return None. |
