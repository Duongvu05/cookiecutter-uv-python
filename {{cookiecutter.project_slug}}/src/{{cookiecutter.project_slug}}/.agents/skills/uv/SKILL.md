---
name: uv
description: uv — Python package manager, dependency management, virtual environments, and script running. Replaces pip, pip-tools, virtualenv, pyenv.
---

# uv

## Project setup

```bash
# Init new project (creates pyproject.toml + .venv)
uv init my-project
cd my-project

# Create venv in existing project
uv venv                        # uses .python-version or pyproject.toml
uv venv --python 3.10          # specific version
```

## Dependency management

```bash
# Add runtime dependency (updates pyproject.toml + uv.lock)
uv add torch numpy pandas

# Add dev/optional dependency
uv add --dev pytest ruff pyright
uv add --optional baselines lightning transformers

# Remove dependency
uv remove numpy

# Upgrade a package
uv add --upgrade numpy

# Install all deps from lockfile (CI / fresh clone)
uv sync
uv sync --all-extras --dev     # include all optional groups + dev

# Low-level install without touching pyproject.toml
uv pip install some-package
```

## Running code

```bash
# Always use uv run — never bare python
uv run python script.py
uv run python -m module.name
uv run pytest tests/
uv run ruff check .
uv run pyright

# Run a one-off tool without installing globally
uvx ruff check .
uvx library-skills --claude
uvx cookiecutter https://github.com/...
```

## Lock file

```bash
uv lock             # regenerate uv.lock from pyproject.toml
uv lock --upgrade   # upgrade all packages to latest compatible
```

## Python version management

```bash
uv python install 3.10 3.11    # install Python versions
uv python pin 3.10             # create .python-version file
uv python list                 # list available versions
```

## uv.sources — custom index / local path

```toml
# pyproject.toml
[tool.uv.sources]
torch = { index = "pytorch" }
my-local-pkg = { path = "../my-local-pkg", editable = true }

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu121"
explicit = true
```

## Pitfalls

- Never use bare `pip install` or `python` in a uv-managed project — always prefix with `uv run` or `uv pip`.
- `uv sync` installs exactly what is in `uv.lock`; `uv add` resolves and updates the lock. Don't mix them carelessly.
- `uv pip install` skips pyproject.toml update — only use for ephemeral/system installs.
- Commit both `pyproject.toml` and `uv.lock` to git for reproducible environments.
- `uvx` runs tools in isolated ephemeral envs — don't use it for project-level tools that need the project venv.
