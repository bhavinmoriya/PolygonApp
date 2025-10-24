import streamlit as st
import folium
from shapely.geometry import Polygon
from streamlit_folium import st_folium
import re
from shapely.wkt import loads
st.set_page_config(layout="wide")
# Streamlit app title
st.title("Polygon Plotter")

# Input for the polygon string
polygon_str = st.text_input(
    "Enter the polygon coordinates (e.g., POLYGON ((9.3270795 48.743215, ...))):",
    "POLYGON ((9.3270795 48.743215, 9.3270795 48.7460675, 9.321068 48.7460675, 9.321068 48.743215, 9.3270795 48.743215))"
)

# Parse the polygon string
# def parse_polygon(polygon_str):
#     # Extract coordinates using regex
#     coords_str = re.search(r"\(\((.*?)\)\)", polygon_str).group(1)
#     coords = [tuple(map(float, pair.split())) for pair in coords_str.split(",")]
#     return coords

try:
    # Parse the input
    coords = parse_polygon(polygon_str)
    # st.write(coords)
    # Parse the polygon string into a Shapely Polygon object
    polygon = loads(polygon_str)
    
    # Extract the coordinates
    coords = list(polygon.exterior.coords)
    # st.write(coords)

    # Create a folium map centered on the polygon
    center_lat = sum(p[1] for p in coords) / len(coords)
    center_lon = sum(p[0] for p in coords) / len(coords)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        # tiles="cartodb positron",
        tiles="openstreetmap"
    )

    # Add the polygon to the map
    folium.GeoJson(
        Polygon(coords),
        style_function=lambda x: {"fillColor": "blue", "color": "blue", "weight": 2, "fillOpacity": 0.2}
    ).add_to(m)

    # Display the map
    st_folium(m, height=800, width=None)

except Exception as e:
    st.error(f"Error parsing polygon: {e}")
