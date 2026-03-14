# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Installation

This project is managed by [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

## Usage

```bash
uv run python src/{{ cookiecutter.project_slug }}/main.py
```

## Development

Run tests with:

```bash
uv run pytest
```
