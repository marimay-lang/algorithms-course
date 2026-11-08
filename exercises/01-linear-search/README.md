# Exercise: index of the first occurrence

Implement linear search for the first element equal to `target`:

```marimay
fn firstIndexOf(values: []int, target: int): Option<int>
```

Put the implementation in `search.my` and tests in `search_test.my` in this
directory. The function may remain package-private: neighboring `_test.my`
files can access it.

## Contract

- If present, return `Some(index)` for the first occurrence.
- If absent, return `None` (or explicitly typed `None<int>()`).
- Indices start at zero.
- Any `int` array, including an empty array, is valid; sorting is not assumed.
- Do not modify the input array.

```text
firstIndexOf([8, 3, 8], 8) == Some(0)
firstIndexOf([8, 3, 8], 3) == Some(1)
firstIndexOf([8, 3, 8], 5) == None
firstIndexOf([], 5)        == None
```

## Completion criteria

1. State the loop invariant in words.
2. Justify runtime and auxiliary memory.
3. Test an empty array, singleton, absent value and duplicates.
4. Pass `mmay fmt . --check`, `mmay check .` and `mmay test . --engine both`.

Make your own attempt before consulting implementations in the reference corpus.
