"""Run inference with trained model."""
from pathlib import Path
import torch
import xarray as xr

from .model import DCRNN


def run_inference(model_path: Path, graph_path: Path, features: torch.Tensor) -> torch.Tensor:
    data = torch.load(graph_path)
    model = DCRNN(features.size(-1), 32, 1)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    with torch.no_grad():
        pred = model(features, data.edge_index, data.edge_attr)
    return pred


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Trained model path")
    parser.add_argument("graph", help="Graph file")
    parser.add_argument("features", help="Dynamic features NetCDF")
    parser.add_argument("--out", default="predictions.nc", help="Output file")
    args = parser.parse_args()

    ds = xr.open_dataset(args.features)
    features = torch.from_numpy(ds.to_array().values.transpose(1, 0)).float()
    preds = run_inference(Path(args.model), Path(args.graph), features)
    ds["aqi_pred"] = ("cell", preds.numpy())
    ds.to_netcdf(args.out)
    print("Saved", args.out)


if __name__ == "__main__":
    main()
