# Cookiecutter UV Python Template

A modern, research-oriented Python project template managed by **uv**. This template scaffolds a complete project structure with built-in agent rules, linting, and automated environment setup.

## 🚀 Quick Start

To create a new project using this template, simply run:

```bash
uv run cookiecutter https://github.com/Duongvu05/cookiecutter-uv-python
```

*Note: You don't need to install cookiecutter globally; `uv` will handle it for you.*

## ✨ Features

- **Modern Dependency Management**: Powered by [uv](https://github.com/astral-sh/uv) for blazing-fast environment synchronization.
- **Automated Setup**: Automatically runs `uv sync` after project generation.
- **Standard Research Structure**: Includes dedicated folders for `.agent`, `.github`, `configs`, `docs`, and `scripts`.
- **Agent-Ready**: Pre-configured with `.agent/rules/base.md` to guide AI coding assistants.
- **Clean Logging**: Uses [loguru](https://github.com/Delgan/loguru) by default (no more `print` for logging).
- **Pro Tooling**: Built-in support for `ruff` (linting/formatting), `pyright` (static analysis), and `pytest` (testing).

## 📁 Project Structure

```text
<project_slug>/
├── .agent/              # AI Agent rules and instructions
│   └── rules/
│       └── base.md
├── .github/             # CI/CD workflows
├── configs/             # Configuration files (YAML, JSON, etc.)
├── docs/                # Project documentation
├── scripts/             # Utility scripts
├── src/                 # Source code
│   └── <project_slug>/
├── pyproject.toml       # Build system and dependencies
└── README.md            # Generated project README
```

## 🛠 Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

## 📝 Customization

You can modify the `cookiecutter.json` in this repository to change default values for:
- Project Name
- Author Details
- Python Version
- Versioning

---
Created by [Duongvu05](https://github.com/Duongvu05)
