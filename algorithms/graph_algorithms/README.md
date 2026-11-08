# Graph algorithms

These finite reference implementations use adjacency lists and zero-based
vertex indices. They do not modify the input or use recursion. Every public
operation validates every endpoint before traversal, including unreachable
rows. A missing path or distance is `None`; no integer is reserved as infinity.

`Adjacency` is `[][]int`. `WeightedAdjacency` is `[][]Edge`, with
`edge(to, weight)` constructing an immutable `Edge`. All operations return
`Result<..., Error>`. Invalid starts and endpoints, an inappropriate graph
kind, cycles, negative cycles, disconnected spanning-tree inputs, and checked
arithmetic overflow are explicit errors. Any unrepresentable intermediate
sum is rejected, even if a later alternative path could avoid it.

Let V be the vertex count and E the number of stored directed entries. On a
valid symmetric graph, symmetry verification costs
U = O(V + E + sum(degree(v)^2)); its general worst-case bound is O(V + E^2).
The direct scans deliberately verify reverse-edge multiplicities and, for
weighted graphs, matching weights. This validation cost is part of the call.

| API | Result value | Full-call time | Auxiliary space |
| --- | --- | --- | --- |
| `dfs` | Discovery order from a start | O(V + E) | O(V) |
| `bfsDistances` | `[]Option<int>` hop counts | O(V + E) | O(V) |
| `bfsPath` | `Option<[]int>` shortest hop path | O(V + E) | O(V) |
| `connectedComponents` | Component labels for a symmetric graph | U | O(V) |
| `topologicalOrder` | Kahn ordering, or `Cycle` | O(V + E) | O(V) |
| `hasDirectedCycle` | Boolean, with malformed inputs still rejected | O(V + E) | O(V) |
| `bipartiteColoring` | Colors 0/1, or `NotBipartite` | U | O(V) |
| `stronglyConnectedComponents` | Kosaraju component labels | O(V + E) | O(V + E) |
| `dagShortestPaths` | Signed-weight single-source distances | O(V + E) | O(V + E) |
| `bellmanFord` | Signed-weight single-source distances | O(V(V + E)) | O(V) |
| `dijkstra` | Nonnegative single-source distances | O(V^2 + E) | O(V) |
| `floydWarshall` | All-pairs optional-distance matrix | O(V^3 + E) | O(V^2) |
| `prim` | `SpanningTree` | U + O(V^2 + E) | O(V) |
| `kruskal` | `SpanningTree` | O(V + E^2) | O(V + E) |

Bellman-Ford rejects negative cycles reachable from its start. Floyd-Warshall
rejects a negative cycle anywhere. Dijkstra rejects a negative edge anywhere,
including an unreachable component. DAG shortest paths require the whole
graph to be acyclic. Arithmetic errors take precedence when a computed
intermediate sum cannot be represented.

`connectedComponents`, `bipartiteColoring`, `prim`, and `kruskal` require exact
undirected symmetry. Parallel edges are supported; self-loops fail bipartite
coloring and are ignored by spanning trees. Negative weights are valid for
MSTs. An empty graph has an empty ordering/component partition/all-pairs
matrix and an empty spanning tree of weight zero. A traversal still needs a
valid start. A nonempty disconnected graph has no spanning tree.

`SpanningTree` exposes `totalWeight` and `edges`; each `TreeEdge` exposes
`source`, `target`, and `weight`. Prim uses a dense selection scan. The
Kruskal reference deliberately uses insertion sort, so it claims O(E^2), not
the O(E log E) cost of a version using an efficient comparison sort.

Tests include all 512 three-vertex directed graphs for mutual-reachability
and SCC relations, independent shortest-path comparisons, every weighted
triangle over three selected weights for exhaustive MST comparison, and
invalid/unreachable inputs, self-loops, parallel edges, empty graphs, and
arithmetic boundaries.
