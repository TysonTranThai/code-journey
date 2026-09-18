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
    mods = [f"csa_m{i}" for i in range(1, 23)] + ["csa_m24"]  # 23 modules (m5 = reflection+attributes)
    for name in mods:
        mod = __import__(name)
        mod.build()

    csa.emit()


if __name__ == "__main__":
    main()
