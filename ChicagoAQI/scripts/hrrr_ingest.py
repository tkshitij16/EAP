"""HRRR data ingestion utilities."""
from pathlib import Path
import pandas as pd
import requests
import xarray as xr


def download_hrrr_hour(date_hour: pd.Timestamp, out_dir: Path) -> Path:
    """Download a single HRRR grib2 file via NOMADS."""
    out_dir.mkdir(parents=True, exist_ok=True)
    url = (
        "https://nomads.ncep.noaa.gov/cgi-bin/filter/hrrr_2d.pl?file=hrrr.t"
        f"{date_hour:%H}z.wrfsfcf00.grib2&subregion=&leftlon=-88&rightlon=-87"
        f"&toplat=42&bottomlat=41&dir=%2Fhrrr.{date_hour:%Y%m%d}"
    )
    out_path = out_dir / f"hrrr_{date_hour:%Y%m%d%H}.grib2"
    if not out_path.exists():
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        out_path.write_bytes(r.content)
    return out_path


def load_hrrr_hours(hours: list[pd.Timestamp], out_dir: Path) -> xr.Dataset:
    """Download and load multiple HRRR hours."""
    files = [download_hrrr_hour(h, out_dir) for h in hours]
    ds = xr.open_mfdataset(files, combine="nested", concat_dim="time")
    return ds


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Download HRRR data")
    parser.add_argument("start", help="start hour YYYY-MM-DD HH")
    parser.add_argument("end", help="end hour YYYY-MM-DD HH")
    parser.add_argument("--out", default="data/hrrr", help="output directory")
    args = parser.parse_args()

    start = pd.to_datetime(args.start)
    end = pd.to_datetime(args.end)
    hours = pd.date_range(start, end, freq="H")
    ds = load_hrrr_hours(hours, Path(args.out))
    out_path = Path(args.out) / "hrrr_subset.nc"
    ds.to_netcdf(out_path)
    print("Saved", out_path)


if __name__ == "__main__":
    main()
