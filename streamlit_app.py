import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Custom styles for dividers
horizontal_line_style = "border: 2px solid #ccc; margin: 20px 0;"
vertical_divider_style = """
    <div style="
        height: 100%;
        width: 2px;
        background-color: #ccc;
        position: absolute;
        left: 50%;
        top: 0;
    "></div>
"""

# Render vertical divider
st.markdown(vertical_divider_style, unsafe_allow_html=True)

# Divide the layout into two main columns (left and right)
col1, col2 = st.columns([1, 1], gap="medium")

# **Left Section: Folium Map**
with col1:
    map_height = 800  # Adjust the height as needed

    # Load the data from the CSV file
    data = pd.read_csv("https://drive.google.com/uc?export=download&id=1hdco3Lnkt7Fz8PlI33A153T9Mt77nUSY")

    # Filter for only Pennsylvania (state 'PA') entries
    data_pa = data[data['state'] == 'PA']

    # Further filter for only restaurants in Philadelphia area
    # Define the approximate bounding box for Philadelphia (adjust as needed)
    philly_bounds = {
        "north": 40.137992,
        "south": 39.867004,
        "east": -74.955763,
        "west": -75.280303
    }
    data_philly = data_pa[
        (data_pa['latitude'] >= philly_bounds['south']) &
        (data_pa['latitude'] <= philly_bounds['north']) &
        (data_pa['longitude'] >= philly_bounds['west']) &
        (data_pa['longitude'] <= philly_bounds['east'])
    ]

    # Initialize the map centered on Philadelphia
    philadelphia_map = folium.Map(location=[39.9526, -75.1652], zoom_start=12)

    # Define grid size (e.g., 0.01 degrees per cell)
    lat_step = 0.01
    lon_step = 0.01

    # Generate grid cells within the bounding box
    lat_bins = np.arange(philly_bounds['south'], philly_bounds['north'], lat_step)
    lon_bins = np.arange(philly_bounds['west'], philly_bounds['east'], lon_step)

    # Loop over each cell in the grid
    for lat in lat_bins:
        for lon in lon_bins:
            # Filter restaurants within this grid cell
            cell_data = data_philly[
                (data_philly['latitude'] >= lat) &
                (data_philly['latitude'] < lat + lat_step) &
                (data_philly['longitude'] >= lon) &
                (data_philly['longitude'] < lon + lon_step)
            ]
            
            # Calculate the average rating for restaurants in this cell
            if len(cell_data) > 0:
                avg_rating = cell_data['stars'].mean()
                avg_rating_text = f"Average Rating: {avg_rating:.2f}"
                
                # Determine color based on average rating with finer gradient
                if avg_rating >= 4.5:
                    color = "#00FF00"  # Green
                elif avg_rating >= 4.0:
                    color = "#7FFF00"  # Lime Green
                elif avg_rating >= 3.5:
                    color = "#FFFF00"  # Yellow
                elif avg_rating >= 3.25:
                    color = "#FFD700"  # Light Orange (Gold)
                elif avg_rating >= 3.0:
                    color = "#FFA500"  # Orange
                elif avg_rating >= 2.5:
                    color = "#FF8C00"  # Dark Orange
                else:
                    color = "#FF0000"  # Red
                
                # Add a rectangle for this grid cell with a tooltip
                folium.Rectangle(
                    bounds=[[lat, lon], [lat + lat_step, lon + lon_step]],
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.2,  # Reduced opacity for better transparency
                    tooltip=avg_rating_text
                ).add_to(philadelphia_map)

    # Render the updated map in the Streamlit interface
    st_folium(philadelphia_map, width=700, height=map_height)

# **Right Section: Charts and Description**
with col2:
    # Top Section: Charts
    chart_col1, chart_col2 = st.columns(2)  # Two charts side by side

    # Plotly Bar Chart (With Dummy Data)
    with chart_col1:
        bar_chart = go.Figure(
            data=[go.Bar(x=["Category A", "Category B", "Category C"], y=[100, 150, 200])],
            layout=go.Layout(title="Bar Chart", xaxis=dict(title="Categories"), yaxis=dict(title="Values"))
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    # Plotly Pie Chart (With Dummy Data)
    with chart_col2:
        pie_chart = go.Figure(
            data=[go.Pie(labels=["Category A", "Category B", "Category C"], values=[30, 50, 20])],
            layout=go.Layout(title="Pie Chart")
        )
        st.plotly_chart(pie_chart, use_container_width=True)

    # Horizontal Separator Line
    st.markdown(f'<div style="{horizontal_line_style}"></div>', unsafe_allow_html=True)

    # Bottom Section: Text Description
    st.write("**Analysis Description**")
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
