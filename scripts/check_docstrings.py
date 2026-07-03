"""Check that public Python modules, classes, and functions have docstrings."""

from __future__ import annotations

import ast
from pathlib import Path


def missing_docstrings() -> list[str]:
    """Return Python objects that do not have docstrings."""

    missing: list[str] = []
    for root in (Path("src"), Path("scripts")):
        for path in sorted(root.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            if ast.get_docstring(tree) is None:
                missing.append(f"{path}: module")
            for node in ast.walk(tree):
                if isinstance(node, (ast.AsyncFunctionDef, ast.ClassDef, ast.FunctionDef)):
                    if ast.get_docstring(node) is None:
                        missing.append(f"{path}:{node.lineno} {node.name}")
    return missing


def main() -> None:
    """Run the docstring check."""

    missing = missing_docstrings()
    if missing:
        print("Missing docstrings:")
        print("\n".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
