"""Build static features for Chicago AQI grid."""
from pathlib import Path
import geopandas as gpd
import rasterio
import pandas as pd
from shapely.geometry import box


def create_fishnet(city_bounds: gpd.GeoDataFrame, cell_size: float) -> gpd.GeoDataFrame:
    xmin, ymin, xmax, ymax = city_bounds.total_bounds
    cols = list(range(int(xmin), int(xmax), int(cell_size)))
    rows = list(range(int(ymin), int(ymax), int(cell_size)))
    polygons = []
    for x in cols:
        for y in rows:
            polygons.append(box(x, y, x + cell_size, y + cell_size))
    fishnet = gpd.GeoDataFrame({"geometry": polygons}, crs=city_bounds.crs)
    return fishnet


def add_landuse(fishnet: gpd.GeoDataFrame, landuse_tif: Path) -> gpd.GeoDataFrame:
    with rasterio.open(landuse_tif) as src:
        landuse = [x[0] for x in src.sample([(geom.centroid.x, geom.centroid.y) for geom in fishnet.geometry])]
    fishnet["landuse"] = landuse
    return fishnet


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("city_shp", help="City boundary shapefile")
    parser.add_argument("landuse", help="Land use raster GeoTIFF")
    parser.add_argument("--out", default="features/static.geojson", help="output file")
    args = parser.parse_args()

    city = gpd.read_file(args.city_shp)
    grid = create_fishnet(city, 500)
    grid = add_landuse(grid, Path(args.landuse))
    grid.to_file(args.out, driver="GeoJSON")
    print("Saved", args.out)


if __name__ == "__main__":
    main()
