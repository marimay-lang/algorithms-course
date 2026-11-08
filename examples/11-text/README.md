# Algorithms over Unicode scalar sequences

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/11-text
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/text_algorithms/).

## Invariant

KMP retains the length of the matching pattern prefix and falls back through its prefix table. The Z window reuses already established prefix equality. Distinct-substring windows start after the last repeated scalar.

## Trace

In λ🙂λ🙂🚀, the pattern 🙂🚀 starts at scalar offset 3. This is not its UTF-8 byte offset. Empty patterns match at zero; equal-length longest spans choose the earliest start.

## Cost

Naive search is O(nm); KMP O(n+m), O(m) space; Z O(n), O(n) space. Center-expansion palindrome search is O(n^2), O(1) space. Run-length encoding is O(n) with O(runs) output; longest-distinct windows are expected O(n) using a last-position map.

## Contract

Inputs are []rune arrays from std/text.runes, whose conversion limit is explicit. All positions/counts are Unicode scalars, without normalization or grapheme segmentation. longestPalindrome returns a half-open RuneSpan; run-length encoding retains rune values and counts.

## Exercise

Implement all overlapping KMP matches. Test 🙂🙂🙂 with pattern 🙂🙂, an empty pattern, and canonically equivalent strings with different scalar sequences.
