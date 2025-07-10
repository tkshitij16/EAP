"""Assemble graph structure for GNN."""

from pathlib import Path
import geopandas as gpd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import torch
from torch_geometric.data import Data


def build_knn_graph(grid_geojson: Path, k: int = 8) -> Data:
    grid = gpd.read_file(grid_geojson)
    coords = np.stack([grid.centroid.x, grid.centroid.y], axis=1)
    nbrs = NearestNeighbors(n_neighbors=k + 1).fit(coords)
    distances, indices = nbrs.kneighbors(coords)
    # skip self neighbor
    edge_index = []
    edge_attr = []
    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        for dist, j in zip(dist_row[1:], idx_row[1:]):
            edge_index.append([i, j])
            edge_attr.append([dist])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)
    data = Data(edge_index=edge_index, edge_attr=edge_attr, num_nodes=len(grid))
    return data


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("grid", help="Grid GeoJSON with features")
    parser.add_argument("--out", default="graphs/graph.pt", help="Output file")
    args = parser.parse_args()

    data = build_knn_graph(Path(args.grid))
    torch.save(data, args.out)
    print("Saved", args.out)


if __name__ == "__main__":
    main()
