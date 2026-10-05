# Security policy

## Supported versions

The project has no releases. Only the latest commit on `main` is supported, and fixes land there.

## Scope

The solutions run locally: each one reads an input file under `inputs/` and prints its answers. Nothing in the repository opens a network connection or runs as a service.

In scope:

- The code in this repository: the day modules, `utils/` and `tests/`.
- The CI workflow and Dependabot configuration under `.github/`.
- A secret, credential or real puzzle input committed by mistake.

A vulnerability in a dependency such as `z3-solver`, `pytest`, `ruff` or `ty` belongs with that project. Report it here as well if this repository uses the affected code in a way that exposes it.

## Reporting a vulnerability

Do not open a public issue or pull request. Report it privately: on the repository's **Security** tab, choose **Report a vulnerability**, or go directly to the [new advisory form](https://github.com/maltemindedal/advent-of-code/security/advisories/new).

Include:

- the affected file, commit or dependency;
- steps to reproduce;
- what an attacker could do with it.
