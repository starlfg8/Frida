#!/usr/bin/env python3
"""Overlay the two rebuilt GLib static libraries onto the matching Frida SDK."""

import hashlib
import sys
import tarfile
from pathlib import Path

NAMES = ("libglib-2.0.a", "libgio-2.0.a")


def overlay(archive_path, sdk_path):
    sdk = Path(sdk_path)
    if not (sdk / "VERSION.txt").is_file():
        raise RuntimeError("The upstream SDK must be extracted before overlaying GLib")
    with tarfile.open(archive_path, "r:xz") as archive:
        for name in NAMES:
            members = [m for m in archive.getmembers() if m.isfile() and m.name.endswith("/" + name)]
            targets = list(sdk.rglob(name))
            if len(members) != 1 or len(targets) != 1:
                raise RuntimeError(f"Expected exactly one source and target for {name}")
            with archive.extractfile(members[0]) as stream:
                data = stream.read()
            targets[0].write_bytes(data)
            print(f"Installed {targets[0]} sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    overlay(sys.argv[1], sys.argv[2])
