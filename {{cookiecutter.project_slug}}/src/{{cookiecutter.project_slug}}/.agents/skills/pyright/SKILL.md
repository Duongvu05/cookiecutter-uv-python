---
name: pyright
description: Pyright static type checker — configuration, common errors, type annotation patterns for Python 3.10+ with uv projects
---

# Pyright

## Running

```bash
uv run pyright                  # check all configured paths
uv run pyright src/my_module/   # check specific path
uv run pyright --version
```

## pyproject.toml config

```toml
[tool.pyright]
pythonVersion = "3.10"
pythonPlatform = "Linux"
typeCheckingMode = "basic"      # off | basic | standard | strict
include = ["src", "baselines"]
exclude = [
    "tests",
    "baselines/tgn",            # submodules with no stubs
    "**/__pycache__",
]
venvPath = "."
venv = ".venv"
reportMissingImports = true
reportMissingTypeStubs = false  # suppress for packages with no stubs (torch, dgl)
```

## Type annotation patterns (Python 3.10+)

```python
from __future__ import annotations  # enables postponed evaluation everywhere

# Union — use X | Y (not Optional[X] or Union[X, Y])
def load(path: str | None = None) -> dict[str, float]:
    ...

# Generics — use lowercase built-ins (Python 3.9+)
def process(items: list[int]) -> dict[str, list[float]]:
    ...

# Callable
from collections.abc import Callable, Sequence
fn: Callable[[int, str], bool]

# TypeVar
from typing import TypeVar
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

# Self (Python 3.11+ or typing_extensions)
from typing import Self
class Builder:
    def set_lr(self, lr: float) -> Self:
        self.lr = lr
        return self

# Type alias
type Vector = list[float]           # Python 3.12+
Vector = list[float]                # Python 3.10 compatible
```

## Suppressing errors

```python
x: int = some_dynamic_value  # type: ignore[assignment]

# Whole file — put at top
# pyright: ignore[reportMissingImports]
```

## Common errors and fixes

| Error | Fix |
|-------|-----|
| `reportMissingImports` for torch/dgl | set `reportMissingTypeStubs = false` or add stub package |
| `Cannot access attribute X` | narrow type with `isinstance` check or cast |
| `Type X is not assignable to Y` | check union types; use `assert isinstance(x, T)` to narrow |
| `reportUnknownMemberType` | add `# type: ignore[reportUnknownMemberType]` for third-party |
| `reportAny` | avoid `Any`; if needed, add comment explaining why |

## Stub packages for common ML libs

```bash
uv add --dev pandas-stubs types-PyYAML types-tqdm
```

## Pitfalls

- `from __future__ import annotations` must be the first import — it makes all annotations strings at runtime, fixing forward-reference issues.
- Pyright uses the venv from `venvPath`/`venv` config; if not set it may miss installed packages.
- `typeCheckingMode = "strict"` requires every function to be fully annotated — start with `"basic"` and tighten gradually.
- Don't use `# type: ignore` without specifying the error code — it silences all errors on that line.
