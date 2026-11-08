# algorithms-course

![Algorithms, step by step — a Marimay learning project](.github/banner.svg)

> **Personal learning project.** This open-source MIT project is part of
> [Marimay](https://github.com/marimay-lang/marimay), my hobby programming-language project.
> I maintain it in my spare time to learn by building. APIs and tooling may
> change, and progress may be intermittent.

A personal algorithms and data-structures course in Marimay. Worked examples live
in `examples/`, exercises in `exercises/`, and theory and progress notes in `notes/`.

**Status:** Early learning material. The current lesson covers a linear scan and a related
linear-search exercise; the curriculum is still growing.

## Run and verify

```sh
mmay fmt . --check
mmay check . --all-targets
mmay run ./examples/01-linear-scan
mmay test ./examples/01-linear-scan --engine both
mkdir -p build
mmay build ./examples/01-linear-scan --release --output build/linear-scan
./build/linear-scan
```

Put a compatible `mmay` on your `PATH`. The original material targets Marimay
`0.1.0-alpha.1` and its `0.1-design` language surface.

The learning loop is to model an input, count operations, trace an example, state
an invariant, implement a related exercise, and check reasoning, formatting,
types and tests. Compare VM and native execution where supported.

## License

[MIT](LICENSE). Existing copyright attribution is retained.
