"""Build dynamic features by interpolating HRRR data to grid centroids."""

from pathlib import Path
import geopandas as gpd
import xarray as xr
import pandas as pd
from scipy.interpolate import griddata


def interpolate_to_grid(hrrr_nc: Path, grid_geojson: Path) -> xr.Dataset:
    grid = gpd.read_file(grid_geojson)
    ds = xr.open_dataset(hrrr_nc)
    lon = ds["longitude"]
    lat = ds["latitude"]
    points = pd.DataFrame({"lon": lon.values.ravel(), "lat": lat.values.ravel()})
    features = {}
    for var in ["u", "v", "temperature", "humidity"]:
        values = ds[var].values.ravel()
        interp = griddata(points.values, values, (grid.centroid.x, grid.centroid.y), method="linear")
        features[var] = interp
    out = xr.Dataset({k: ("cell", v) for k, v in features.items()}, coords={"cell": grid.index})
    return out


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("hrrr_nc", help="HRRR NetCDF file")
    parser.add_argument("grid", help="Grid GeoJSON")
    parser.add_argument("--out", default="features/dynamic.nc", help="Output file")
    args = parser.parse_args()

    ds = interpolate_to_grid(Path(args.hrrr_nc), Path(args.grid))
    ds.to_netcdf(args.out)
    print("Saved", args.out)


if __name__ == "__main__":
    main()
