# Local course verification — 2026-11-08

The [machine-readable report](verification-2026-11-08.json) records the exact
Marimay source/lesson-manifest digest and compiler binary SHA-256 used for this
run on macOS arm64. It was generated before committing the course expansion;
`repository_revision` is the base checkout, and `working_tree_dirty: true`
explicitly identifies the tested working-tree snapshot.

- Formatting and `check --all-targets` passed.
- All 66 declared tests passed with `test --engine both`.
- All 12 numbered lessons passed in the VM and as native debug/release programs,
  with exact expected stdout.
- The verifier's 14 Python unit tests passed.

The compiler was copied together with its debug/release native archives,
matching manifests and headers into an installed-layout snapshot before this
successful run. This prevented a concurrent compiler rebuild from changing
the executable or runtime files during verification. The binary hash identifies
the executable; no source-build provenance is inferred for the frozen copy.

The tests include exhaustive short arrays and texts, independent subset and
interval oracles, all three-vertex directed graphs, cross-checked shortest paths
and spanning trees, invalid inputs, Unicode scalar offsets, integer boundaries,
and range-update rollback on overflow. These checks are finite correctness
evidence for the recorded build, not a performance result or a language-release
acceptance claim.

Reproduce on a compatible current compiler from the course root:

```sh
MMAY=/absolute/path/to/mmay python3 tools/verify_algorithms.py \
  --output build/verification.json
python3 -m unittest discover -s tools -p 'test_*.py'
```
