import streamlit as st
import folium
from shapely.geometry import Polygon
from streamlit_folium import st_folium
import re
from shapely.wkt import loads
# st.set_page_config(layout="wide")

st.set_page_config(page_title="Polygon Plotter - Up to 4 Polygons", layout="wide")  # Unique browser tab title
# Streamlit app title
st.title("Polygon Plotter - Up to 4 Polygons")

# Input for multiple polygons
st.write("### Enter up to 4 polygon coordinates (one per text area):")

polygon_inputs = []
colors = ["blue", "red", "green", "orange"]

for i in range(4):
    default_polygon = "POLYGON ((9.3270795 48.743215, 9.3270795 48.7460675, 9.321068 48.7460675, 9.321068 48.743215, 9.3270795 48.743215))" if i == 0 else ""
    
    polygon_str = st.text_area(
        f"Polygon {i+1} ({colors[i]}):",
        value=default_polygon,
        height=100,
        key=f"polygon_{i}"
    )
    
    if polygon_str.strip():
        polygon_inputs.append((polygon_str, colors[i]))

# Process all polygons
if polygon_inputs:
    try:
        all_polygons = []
        all_coords = []
        
        # Parse all polygons
        for polygon_str, color in polygon_inputs:
            polygon = loads(polygon_str)
            coords = list(polygon.exterior.coords)
            all_polygons.append((polygon, coords, color))
            all_coords.extend(coords)
        
        # Calculate bounds for all polygons
        if all_coords:
            min_lat = min(coord[1] for coord in all_coords)
            max_lat = max(coord[1] for coord in all_coords)
            min_lon = min(coord[0] for coord in all_coords)
            max_lon = max(coord[0] for coord in all_coords)
            
            st.write(f"### Bounds for all polygons: min_lat={min_lat:.6f}, max_lat={max_lat:.6f}, min_lon={min_lon:.6f}, max_lon={max_lon:.6f}")
            
            # Create a folium map centered on all polygons
            center_lat = (min_lat + max_lat) / 2
            center_lon = (min_lon + max_lon) / 2

            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=12,
                tiles="openstreetmap"
            )

            # Add each polygon to the map with different colors
            for i, (polygon, coords, color) in enumerate(all_polygons):
                folium.GeoJson(
                    polygon,
                    style_function=lambda x, c=color: {
                        "fillColor": c, 
                        "color": c, 
                        "weight": 2, 
                        "fillOpacity": 0.3
                    },
                    popup=f"Polygon {i+1}"
                ).add_to(m)

            # Display the map
            st_folium(m, height=800, width=None)
            
            # Show summary
            st.write(f"### Successfully plotted {len(all_polygons)} polygon(s)")
            
    except Exception as e:
        st.error(f"Error parsing polygons: {e}")
else:
    st.info("Please enter at least one polygon to display on the map.")
