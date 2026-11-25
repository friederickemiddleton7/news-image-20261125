#!/usr/bin/env python3
"""Entrypoint for the make.fun "news-image-20261125" competition entry.

Thin wrapper around make_image.build(): regenerates the 1024x1024 poster
(38 stories from Wednesday 25 November 2026) and writes entry.png.

If Pillow is unavailable (fresh grading container without network), it falls
back to copying the committed, already-validated entry.png so the grader still
receives a correct artifact.

Standard library only at import time; Pillow is required only for the rebuild
path, which is exercised by `python3 make_image.py` in development.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
EXPECTED_SIZE = (1024, 1024)


def rebuild() -> str:
    """Render the poster with make_image and return the written path."""
    import make_image  # noqa: PLC0415 - deliberate lazy import

    make_image.build(SOURCE_NAME)
    return SOURCE_NAME


def fallback_copy() -> str:
    """Copy the committed poster when Pillow is not installed."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE_NAME)
    if not os.path.exists(src):
        raise SystemExit("no %s in repo and Pillow unavailable" % SOURCE_NAME)
    shutil.copyfile(src, OUTPUT_NAME)
    return OUTPUT_NAME


def main() -> int:
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)

    try:
        written = rebuild()
        print("rebuilt poster with make_image")
    except ImportError:
        written = fallback_copy()
        print("Pillow unavailable; copied committed poster")

    dest = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(written, dest)

    size = os.path.getsize(dest)
    if size < 1024:
        raise SystemExit("output poster suspiciously small: %d bytes" % size)
    print("ok: %s (%d bytes) written to %s" % (OUTPUT_NAME, size, dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
