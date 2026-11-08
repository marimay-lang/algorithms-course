# Graph structure, paths and spanning trees

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/08-graphs
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/graph_algorithms/).

## Invariant

A traversal marks each discovered vertex once. Topological removal consumes only zero-indegree vertices. Relaxation stores the best known reachable distance; a missing distance is represented by None rather than a finite sentinel.

## Trace

Compare an unweighted BFS path with weighted shortest paths on a four-node graph. Add an isolated vertex, then an invalid edge inside its component; validation must reject that edge even if it is unreachable from the chosen source.

## Cost

Directed DFS/BFS and Kahn order are O(V+E); iterative Kosaraju also O(V+E). Undirected validation additionally checks reverse-edge multiplicities by scanning adjacency rows: its cost U is O(sum over edges (deg(u)+deg(v))), or O(E*maximumDegree). Connected components, coloring and spanning-tree calls include this validation cost in addition to their core algorithms. Array-based shortest paths and spanning routines have representation-specific costs recorded in the catalogue. Bellman-Ford here scans vertices on every pass and is O(V*(V+E)); Kruskal uses insertion sorting, so its edge sorting is O(E^2). Floyd-Warshall O(V^3) with O(V^2) distance storage.

## Contract

Vertex indices are zero-based. Entire inputs are validated, including unreachable edges. Undirected algorithms require symmetric adjacency/weights. Negative cycles, disconnected spanning trees, invalid endpoints and arithmetic overflow have explicit errors. Native implementations use explicit stacks instead of recursion.

## Exercise

For all directed three-vertex graphs, compare SCC membership with mutual reachability. Explain why a negative cycle outside the source component affects all-pairs queries differently from a source-specific shortest-path query.
