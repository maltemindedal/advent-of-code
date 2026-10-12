# Day scripts on samples

## Sub-features

- `run("sample")` for every `<year>/<DD>/main.py`, printing `Part 1:` and `Part 2:` lines.

## How to get to it (user POV)

`uv run python -c "import runpy; runpy.run_path('2025/01/main.py')['run']('sample')"`

## Driving it with verify.sh

`verify.sh days`. Every day must exit 0 and print its pinned
`EXPECTED_SAMPLE_OUTPUT` byte for byte.

## Gotchas

- Pinned quirks are deliberate: day 8 prints `Part 1: 20`, day 11 prints `Part 2: 0`, and day 12 prints one `Solution:` line.
