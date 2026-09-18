"""Emit the C# Advanced course. Run from repo root:
python3 scripts/content-authoring/csa_emit.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import csa  # noqa: E402


def main() -> None:
    # Content modules (order does not matter; ids are validated globally).
    import csa_m1  # noqa: F401

    csa_m1.build()

    csa.emit()


if __name__ == "__main__":
    main()
