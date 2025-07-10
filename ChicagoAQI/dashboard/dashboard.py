"""Simple Streamlit dashboard for AQI predictions."""
import streamlit as st
import geopandas as gpd
import xarray as xr
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data(grid_path: str, pred_path: str):
    grid = gpd.read_file(grid_path)
    ds = xr.open_dataset(pred_path)
    grid["aqi"] = ds["aqi_pred"].values
    return grid

st.title("Chicago AQI Predictions")

grid_file = st.sidebar.text_input("Grid file", "../features/static.geojson")
pred_file = st.sidebar.text_input("Predictions", "../predictions.nc")

grid = load_data(grid_file, pred_file)
fig = px.choropleth_mapbox(
    grid,
    geojson=grid.geometry.__geo_interface__,
    locations=grid.index,
    color="aqi",
    center={"lat": 41.88, "lon": -87.63},
    mapbox_style="carto-positron",
    zoom=9,
)
st.plotly_chart(fig, use_container_width=True)
