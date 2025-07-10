"""CLI orchestrator for AQI pipeline."""

import argparse
from pathlib import Path

from scripts.hrrr_ingest import load_hrrr_hours
from scripts.aqs_ingest import load_aqs_data
from scripts.build_static import create_fishnet, add_landuse
from scripts.build_dynamic import interpolate_to_grid
from scripts.graph_assembly import build_knn_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="AQI GNN pipeline")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("ingest-hrrr")
    sub.add_parser("ingest-aqs")
    sub.add_parser("build-static")
    sub.add_parser("build-dynamic")

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()


if __name__ == "__main__":
    main()
