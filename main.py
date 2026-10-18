"""Backwards-compatible launcher: `python main.py` still works."""

from smilebrightness.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
