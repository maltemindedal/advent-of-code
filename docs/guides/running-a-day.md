# Running a day

How to run a solution against your real input, the committed sample or any other input file, and how to call its functions with non-default arguments. Run every command from the repository root.

The file layout and naming rules for inputs are in [API reference: input file layout](../reference/api.md#input-file-layout).

## Run against your real input

Save your input as `inputs/<year>/<DD>.txt`, then run the module as a script:

```bash
uv run python 2025/07/main.py
```

```text
Part 1: <answer>
Part 2: <answer>
```

Running as a script always reads the real input; it has no flags.

## Run against the sample

Call `run` with the variant name:

```bash
uv run python -c "import runpy; runpy.run_path('2025/07/main.py')['run']('sample')"
```

```text
Part 1: 21
Part 2: 40
```

The expected sample output for every 2025 day is listed in [Day modules: 2025 sample output](../reference/day-modules.md#2025-sample-output).

## Run against another input file

Save the file next to the real input with a variant suffix, for example `inputs/2025/07.edge-case.txt`, and pass the suffix to `run`:

```bash
uv run python -c "import runpy; runpy.run_path('2025/07/main.py')['run']('edge-case')"
```

Git ignores every variant except `sample`, so the file stays on your machine.

## Call the functions from Python

Use this when you need an argument that `run` does not pass, or the parsed data itself. `runpy.run_path` returns the module's namespace as a `dict`:

```python
import runpy

from utils import read_input_lines

day08 = runpy.run_path("2025/08/main.py")
points = day08["parse_input"](read_input_lines(2025, 8, "sample"))
print(day08["part1"](points, pairs_to_connect=10))  # 40, the puzzle's example answer
```

Save this as a file and run it with `uv run python <file>` from the repository root; the path passed to `run_path` is relative to the working directory. The parameters each day's `part1` and `part2` accept are listed in [Day modules: 2025 entry points](../reference/day-modules.md#2025-entry-points).

`runpy.run_path` does not execute the module's `if __name__ == "__main__":` block, so loading a module prints nothing by itself.

## Troubleshooting

| Error | Cause | Fix |
| --- | --- | --- |
| `FileNotFoundError: Input for 2025 day 7 not found at .../inputs/2025/07.txt` | The input file is missing or misnamed. | Save it at the path in the message. The day is zero-padded: `07.txt`, not `7.txt`. |
| `ModuleNotFoundError: No module named 'utils'` | The script ran with a Python outside the project environment, or `uv run` was called from outside the repository. | Run `uv run python` from inside the repository; run `uv sync` first if `.venv/` is missing. |
| `FileNotFoundError: [Errno 2] No such file or directory: '<cwd>/2025/07/main.py'` | `runpy.run_path` got a relative path from another directory. | Run from the repository root, or pass an absolute path. |
