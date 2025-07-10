"""EPA AQS ingestion script."""

from pathlib import Path
import pandas as pd
import requests

AQS_URL = "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_site_2025.csv"


def download_aqs_data(out_dir: Path) -> Path:
    """Download EPA AQI data for 2025."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "aqs_2025.csv"
    if not out_path.exists():
        r = requests.get(AQS_URL, timeout=60)
        r.raise_for_status()
        out_path.write_bytes(r.content)
    return out_path


def load_aqs_data(out_dir: Path) -> pd.DataFrame:
    """Return EPA AQI data as DataFrame."""
    path = download_aqs_data(out_dir)
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download EPA AQS AQI data")
    parser.add_argument("--out", default="data/aqs", help="output directory")
    args = parser.parse_args()

    df = load_aqs_data(Path(args.out))
    print(df.head())
