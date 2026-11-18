"""python -m unvibecode_graph REPO [--out DIR] [--open]"""
from __future__ import annotations

import argparse

from .config import VERSION, Config
from .pipeline import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m unvibecode_graph", description="Build the connected code graph of a repository.")
    parser.add_argument("repo", help="repository folder to scan")
    parser.add_argument("--out", default="unvibecode_graph_results", help="folder for run outputs (default: %(default)s)")
    parser.add_argument("--open", action="store_true", help="open the interactive graph in a browser when done")
    args = parser.parse_args(argv)

    print("[SHIPREADYV2 FAST LANE REPOSITORY GRAPH RUN]")
    print(f"Runner version:    {VERSION}")
    print(f"Target repository: {args.repo}")
    print(f"Reports folder:    {args.out}")
    result = run(args.repo, args.out, Config(open_browser=args.open))
    print(f"\nOpen: {result.run_dir / 'fast_lane_symbol_resolution_graph.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
