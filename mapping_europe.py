import pandas as pd
import folium

# Load the datasets
france_data = pd.read_csv('/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/datasets/filtered_france_data.csv')
bird_outbreaks = pd.read_csv('/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/datasets/bird_outbreaks.csv')

# Filter bird_outbreaks to exclude France
bird_outbreaks_europe = bird_outbreaks[bird_outbreaks['Country'] != 'France']

# Prepare France and Europe outbreak data for spatial visualization
france_data_geo = france_data[['Latitude', 'Longitude']].dropna()
europe_data_geo = bird_outbreaks_europe[['Latitude', 'Longitude']].dropna()

# Create an interactive map centered on Europe
m = folium.Map(location=[54.5260, 15.2551], zoom_start=4, tiles='CartoDB positron')

# Add France outbreak points
for _, row in france_data_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup="France Outbreak"
    ).add_to(m)

# Add Europe outbreak points (excluding France)
for _, row in europe_data_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color='blue',
        fill=True,
        fill_opacity=0.4,
        popup="Europe Outbreak"
    ).add_to(m)

# Save the map as an HTML file for visualization
map_file_path = "/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/Outbreak_Spatial_Distribution.html"
m.save(map_file_path)

print(f"Map saved to: {map_file_path}")


