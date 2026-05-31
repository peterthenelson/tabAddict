#!/usr/bin/env python3
"""Package the extension into a zip for Chrome Web Store submission."""

import json
import zipfile
from pathlib import Path

EXTENSION_FILES = [
    "manifest.json",
    "background.js",
    "launch.html", "launch.js", "launch.css",
    "dnd.html", "dnd.js", "dnd.css",
    "options.html", "options.css",
    "icon_open.svg", "icon_capture.svg", "icon_launch.svg",
    "icon-16.png", "icon-32.png", "icon-64.png", "icon-128.png", "icon-256.png",
]

root = Path(__file__).parent
version = json.loads((root / "manifest.json").read_text())["version"]
out = root / f"tabAddict-v{version}.zip"

with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for name in EXTENSION_FILES:
        zf.write(root / name, name)

print(f"Wrote {out.name}  ({out.stat().st_size:,} bytes)")
