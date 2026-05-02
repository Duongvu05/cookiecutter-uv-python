---
name: ruff
description: Ruff — fast Python linter and formatter replacing flake8, black, isort. Configuration, rule selection, and common fixes.
---

# Ruff

## Running

```bash
uv run ruff check .                   # lint
uv run ruff check --fix .             # lint + auto-fix safe fixes
uv run ruff check --fix --unsafe-fixes .  # include unsafe fixes
uv run ruff format .                  # format (like black)
uv run ruff format --check .          # format check only (CI)
uv run ruff check --select ALL .      # see all possible violations
```

## pyproject.toml config

```toml
[tool.ruff]
target-version = "py310"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes (undefined names, unused imports)
    "I",    # isort (import ordering)
    "UP",   # pyupgrade (modernize syntax)
    "B",    # flake8-bugbear (common bugs)
    "SIM",  # flake8-simplify
    "N",    # pep8-naming
    "RUF",  # ruff-specific rules
]
ignore = [
    "E501",   # line too long (formatter handles this)
    "N802",   # lowercase function names (math notation)
    "N803",   # lowercase argument names
    "N806",   # lowercase variable in function
    "B905",   # zip without strict=True
    "SIM108", # ternary over if-else
]

# Per-file ignores
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]          # allow assert in tests
"scripts/*" = ["T201"]        # allow print in scripts

[tool.ruff.lint.isort]
known-first-party = ["stgraph_fs"]
```

## Common rule codes

| Code | Rule | Description |
|------|------|-------------|
| `F401` | unused-import | Imported but unused |
| `F841` | unused-variable | Assigned but never used |
| `E711` | comparison-to-none | Use `is None` not `== None` |
| `UP006` | deprecated-collection-type | `List[x]` → `list[x]` |
| `UP007` | deprecated-union | `Optional[x]` → `x \| None` |
| `B006` | mutable-default-arg | Mutable default in function def |
| `B007` | unused-loop-var | Loop variable unused (use `_`) |
| `I001` | unsorted-imports | Imports not sorted per isort |
| `RUF010` | explicit-f-string | `str(x)` inside f-string → `{x!s}` |

## Inline suppression

```python
import os  # noqa: F401          — suppress specific rule
x = 1      # noqa                 — suppress all rules on line (avoid)
```

## Auto-fixable patterns

Ruff auto-fixes many `UP` rules:

```python
# Before (ruff --fix)
from typing import List, Optional, Dict
def f(x: Optional[int]) -> List[Dict[str, int]]:
    ...

# After
def f(x: int | None) -> list[dict[str, int]]:
    ...
```

## Pitfalls

- `ruff format` and `ruff check --fix` are separate commands — run both.
- `select = ["ALL"]` enables experimental rules; always pin `ignore` list before using in CI.
- `line-length` in `[tool.ruff]` applies to the formatter; set it in `[tool.ruff.lint]` too if using `E501`.
- Ruff's isort is not 100% compatible with standalone isort — if migrating, run `ruff check --select I --fix` to reconcile.
- Per-file ignores use glob patterns relative to the project root, not the file location.
