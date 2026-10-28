#!/usr/bin/env python3
"""Verify the packaged Android SDK contains both patched GLib archives."""

import sys
import tarfile
from pathlib import Path


def verify(path):
    checks = {
        "libglib-2.0.a": b"httpdns_db1\0",
        "libgio-2.0.a": b"gws-1\0",
    }
    if Path(path).is_dir():
        for name, marker in checks.items():
            matches = list(Path(path).rglob(name))
            if len(matches) != 1 or marker not in matches[0].read_bytes():
                raise RuntimeError(f"Expected exactly one patched {name}, found {matches}")
            print(f"Verified extracted {matches[0]}: {marker!r}")
        return
    with tarfile.open(path, "r:xz") as archive:
        members = archive.getmembers()
        for name, marker in checks.items():
            matches = [member for member in members if member.isfile() and member.name.endswith("/" + name)]
            if len(matches) != 1:
                raise RuntimeError(f"Expected exactly one {name}, found {len(matches)}")
            with archive.extractfile(matches[0]) as stream:
                if marker not in stream.read():
                    raise RuntimeError(f"Missing {marker!r} in {name}")
            print(f"Verified {name}: {marker!r}")


if __name__ == "__main__":
    verify(sys.argv[1])
