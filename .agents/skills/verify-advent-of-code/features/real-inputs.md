# Day scripts on real inputs

## Sub-features

- `run()` with no variant reads `inputs/<year>/<DD>.txt`.

## How to get to it (user POV)

The owner saves a real input locally (git-ignored) and runs the day.

## Driving it with verify.sh

`verify.sh real` runs each day that has a real input and checks that it exits 0.
Without any real inputs it prints SKIP.

## Gotchas

- Never commit real inputs or `git add -f` under `inputs/`. No expected real answers exist in the repo.
