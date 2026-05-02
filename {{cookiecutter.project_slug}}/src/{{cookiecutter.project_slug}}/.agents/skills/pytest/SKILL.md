---
name: pytest
description: pytest — test structure, fixtures, markers, parametrize, conftest, and pytest-watch for automated testing in uv projects
---

# pytest

## Running tests

```bash
uv run pytest                          # all tests
uv run pytest tests/                   # specific dir
uv run pytest tests/test_metrics.py    # specific file
uv run pytest -k "test_auc"            # filter by name pattern
uv run pytest -m "not slow"            # exclude marked tests
uv run pytest -v --tb=short            # verbose + short tracebacks
uv run pytest --maxfail=1              # stop after first failure
uv run pytest -x                       # same as --maxfail=1

# Watch mode (re-runs on file save)
uv run ptw                             # requires pytest-watch
uv run ptw -- -m "not slow"            # pass args to pytest
```

## pyproject.toml config

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow (deselect with -m 'not slow')",
    "integration: marks integration tests requiring real data",
]
```

## Test structure

```python
# tests/test_metrics.py
from __future__ import annotations
import pytest
import numpy as np
from stgraph_fs.evaluation.metrics import compute_auc

def test_perfect_auc() -> None:
    labels = np.array([0, 0, 1, 1])
    scores = np.array([0.1, 0.2, 0.8, 0.9])
    assert compute_auc(labels, scores) == pytest.approx(1.0)

def test_random_auc() -> None:
    rng = np.random.default_rng(42)
    labels = rng.integers(0, 2, size=100)
    scores = rng.random(100)
    auc = compute_auc(labels, scores)
    assert 0.4 < auc < 0.6   # random classifier ≈ 0.5
```

## Fixtures (conftest.py)

```python
# tests/conftest.py
from __future__ import annotations
import pytest
import numpy as np

@pytest.fixture
def sample_graph():
    """Small 10-node graph for unit tests."""
    import dgl, torch
    g = dgl.rand_graph(10, 30)
    g.ndata["feat"] = torch.randn(10, 16)
    return g

@pytest.fixture(scope="session")
def real_dataset(tmp_path_factory):
    """Loaded once per session — expensive fixture."""
    tmp = tmp_path_factory.mktemp("data")
    # load / generate dataset once
    return load_elliptic(tmp)
```

## Parametrize

```python
@pytest.mark.parametrize("tau,expected", [
    (0.1, True),
    (0.5, True),
    (1.1, False),
])
def test_tau_validation(tau: float, expected: bool) -> None:
    from stgraph_fs.config import Config
    if expected:
        Config(tau=tau)
    else:
        with pytest.raises(ValueError):
            Config(tau=tau)
```

## Markers

```python
@pytest.mark.slow
def test_full_training_loop() -> None:
    ...

@pytest.mark.integration
def test_loads_real_data() -> None:
    ...

# Skip conditionally
@pytest.mark.skipif(not torch.cuda.is_available(), reason="no GPU")
def test_cuda_forward() -> None:
    ...
```

## Assertion helpers

```python
# Float comparison
assert result == pytest.approx(0.95, abs=1e-3)
assert result == pytest.approx(0.95, rel=0.01)   # 1% relative tolerance

# Exception
with pytest.raises(ValueError, match="tau must be"):
    Config(tau=2.0)

# Warning
with pytest.warns(UserWarning, match="deprecated"):
    old_api()
```

## pytest-watch (file watcher)

```bash
# Install
uv add --dev pytest-watch

# Run — re-executes tests on any .py file change
uv run ptw
uv run ptw tests/                    # watch specific dir
uv run ptw -- -m "not slow" -x       # pass pytest args after --
```

## Pitfalls

- `conftest.py` is auto-discovered — never import it directly.
- Fixtures with `scope="session"` are shared across all tests; don't mutate them in individual tests.
- `pytest.approx` is required for float comparisons — never use `==` on floats directly.
- Avoid `import *` in tests; explicit imports make failures easier to trace.
- `addopts` in pyproject.toml applies to every run; don't put `-x` or `--maxfail` there permanently.
