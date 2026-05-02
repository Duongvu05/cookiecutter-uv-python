import subprocess
import sys


def run(command: list[str], description: str) -> bool:
    print(f"  {description}...")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  FAILED: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"  SKIPPED: '{command[0]}' not found")
        return False


def main() -> None:
    print("\n[post-gen] Setting up project...\n")

    run(["uv", "sync", "--dev"], "Installing dependencies (uv sync --dev)")

    run(["uv", "run", "pre-commit", "install"], "Installing pre-commit hooks")

    # Install agent skills from the package into .claude/skills/
    run(
        ["uvx", "library-skills", "--claude", "--yes"],
        "Installing agent skills (uvx library-skills --claude)",
    )

    print("\n[post-gen] Done! Next steps:")
    print("  uv run pytest          — run tests")
    print("  uv run ptw             — watch mode (re-run on file save)")
    print("  uv run ruff check .    — lint")
    print("  uv run pyright         — type check")
    print("  git init && git add .  — start versioning\n")


if __name__ == "__main__":
    main()
