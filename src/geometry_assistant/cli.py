#!/usr/bin/env python3
"""CLI entry point for geometry-assistant.

Usage:
    geometry-assistant <json_file> [--output <path>] [--serve]
"""
import argparse
import json
import sys
from pathlib import Path

from geometry_assistant.core import (
    build_standalone_html,
    validate_geometry_data,
    start_server,
    _ensure_port_free,
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Export geometryData as a standalone HTML page."
    )
    parser.add_argument(
        "json_file", help="Path to geometryData JSON file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output HTML path (default: geometry_skill/index.html under system temp)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start a local HTTP preview server (requires Node.js)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    data_file = Path(args.json_file)
    if not data_file.exists():
        print(f"JSON file does not exist: {data_file}", file=sys.stderr)
        sys.exit(1)

    with data_file.open("r", encoding="utf-8-sig") as f:
        geom_data = json.load(f)

    try:
        validate_geometry_data(geom_data)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    out_file = Path(args.output) if args.output else (
        Path(tempfile.gettempdir()) / "geometry_skill" / "index.html"
    )
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(build_standalone_html(geom_data), encoding="utf-8")

    if args.serve:
        _ensure_port_free()
        start_server(str(out_file.parent))
        print(f"http://localhost:8080")
    else:
        print(str(out_file.resolve()))


if __name__ == "__main__":
    main()
