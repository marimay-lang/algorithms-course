# Comparison and distribution sorting

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/03-sorting
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/sorting/).

## Invariant

Insertion/selection maintain a finished prefix; merge sort combines adjacent sorted runs; quicksort partitions around a pivot; heap sort repeatedly removes the maximum from its heap prefix. Iterative worklists replace recursive calls.

## Trace

Trace [3,-1,3,0] to [-1,0,3,3]. In a three-way partition all equal pivots occupy one finished interval, preventing duplicate-heavy inputs from repeatedly revisiting those positions.

## Cost

Selection, bubble, cocktail, gnome and insertion are O(n^2). Comb/Shell worst cases depend on their gap schedules and remain O(n^2) for these implementations. Merge and heap sort are O(n log n); iterative quicksort has O(n^2) worst case. Distribution-sort costs and key domains are listed in the catalogue and source comments.

## Contract

Comparison sorts mutate their input array and accept the full signed-int range. Distribution sorts have explicit domain/allocation errors; inspect the signature before use. Stable order cannot be observed on bare equal integers, so do not infer a record-sort stability contract from these tests.

## Exercise

Write tagged-key test data to investigate stability. Explain why an iterative quicksort still needs a worklist and how three-way partitioning handles all-equal input.
