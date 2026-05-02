---
name: pre-commit
description: pre-commit — git hook framework for automating ruff, pyright, pytest, and other checks before every commit
---

# pre-commit

## Setup

```bash
uv add --dev pre-commit
uv run pre-commit install          # installs hook into .git/hooks/pre-commit
uv run pre-commit install --hook-type commit-msg  # optional: commit message hook
```

## Standard config for this project (.pre-commit-config.yaml)

```yaml
repos:
  # Ruff: lint + format
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Pyright: type checking
  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.360
    hooks:
      - id: pyright
        additional_dependencies:
          - pydantic>=2.0
          - numpy>=1.24,<2
          - pandas>=2.0
          - torch>=2.0

  # Pytest: unit tests only (fast; skip slow/integration)
  - repo: local
    hooks:
      - id: pytest-fast
        name: pytest (unit tests)
        entry: uv run pytest
        args: [tests/, -m, "not slow and not integration", --maxfail=1, -q]
        language: system
        pass_filenames: false
        always_run: true
```

## Running manually

```bash
uv run pre-commit run --all-files       # run all hooks on all files
uv run pre-commit run ruff --all-files  # run single hook
uv run pre-commit run --files src/stgraph_fs/config.py  # specific file
uv run pre-commit autoupdate            # update all hook revisions to latest
```

## Skipping hooks (emergency only)

```bash
git commit --no-verify -m "wip: skip hooks"
SKIP=pyright git commit -m "skip pyright only"
```

## Hook types

```yaml
- id: my-hook
  stages: [pre-commit]      # default — runs on git commit
  stages: [pre-push]        # runs on git push (better for slow tests)
  stages: [commit-msg]      # runs on commit message
```

## Running slow tests at pre-push instead of pre-commit

```yaml
  - repo: local
    hooks:
      - id: pytest-full
        name: pytest (all tests)
        entry: uv run pytest tests/ --maxfail=1 -q
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-push]   # only on git push, not every commit
```

```bash
uv run pre-commit install --hook-type pre-push
```

## CI — run pre-commit in GitHub Actions

```yaml
- name: Run pre-commit
  uses: pre-commit/action@v3.0.1
```

## Pitfalls

- `pass_filenames: false` is required for pytest/pyright — they don't accept file args the same way linters do.
- `always_run: true` is needed for hooks that don't filter by file type (pytest, pyright).
- `additional_dependencies` in pyright hook must list packages that pyright needs to type-check — these are installed into the hook's isolated venv, not your project venv.
- Use `language: system` (not `python`) for hooks that should use your project's uv venv.
- Avoid running the full test suite in `pre-commit` (slow); use markers to run only fast unit tests, move integration tests to `pre-push` or CI.
