#!/usr/bin/env python3
"""Unified entry point for the Codex CLI in Python."""
import os
import sys
import subprocess
from pathlib import Path

# Determine whether the user explicitly wants the Rust CLI.
wants_native = Path(__file__).with_name("use-native").exists() or (
    os.getenv("CODEX_RUST") is not None
    and os.getenv("CODEX_RUST").lower() in {"1", "true", "yes"}
)

if wants_native:
    platform = sys.platform
    arch = os.uname().machine

    target_triple = None
    if platform.startswith("linux"):
        if arch == "x86_64":
            target_triple = "x86_64-unknown-linux-musl"
        elif arch == "aarch64":
            target_triple = "aarch64-unknown-linux-musl"
    elif platform == "darwin":
        if arch == "x86_64":
            target_triple = "x86_64-apple-darwin"
        elif arch == "arm64":
            target_triple = "aarch64-apple-darwin"

    if not target_triple:
        raise RuntimeError(f"Unsupported platform: {platform} ({arch})")

    binary_path = Path(__file__).resolve().parent.parent / "bin" / f"codex-{target_triple}"
    result = subprocess.run([str(binary_path), *sys.argv[1:]])
    sys.exit(result.returncode)

# Fallback: execute the original JavaScript CLI
cli_path = Path(__file__).resolve().parent.parent / "dist" / "cli.js"
try:
    subprocess.run(["node", str(cli_path), *sys.argv[1:]], check=True)
except subprocess.CalledProcessError as err:
    print(err, file=sys.stderr)
    sys.exit(err.returncode)
