import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
france_data = pd.read_csv('/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/datasets/filtered_france_data.csv')
bird_outbreaks = pd.read_csv('/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/datasets/bird_outbreaks.csv')
vaccination_intervals = pd.read_csv('/Users/juliettewilliamson/Desktop/going_viral/duckduckgoose/datasets/duck_vaccination_intervals.csv')

# Filter bird_outbreaks to exclude France
bird_outbreaks_europe = bird_outbreaks[bird_outbreaks['Country'] != 'France']

# Preprocess dates and aggregate outbreak counts for France and Europe
france_data['Observation.date'] = pd.to_datetime(france_data['Observation.date'], errors='coerce')
bird_outbreaks_europe['Observation.date'] = pd.to_datetime(bird_outbreaks_europe['Observation.date'], errors='coerce')

# Group data by month and count events
france_trends = france_data.groupby(france_data['Observation.date'].dt.to_period('M')).size().reset_index(name='Outbreaks')
europe_trends = bird_outbreaks_europe.groupby(bird_outbreaks_europe['Observation.date'].dt.to_period('M')).size().reset_index(name='Outbreaks')

# Convert period to datetime for plotting
france_trends['Observation.date'] = france_trends['Observation.date'].dt.to_timestamp()
europe_trends['Observation.date'] = europe_trends['Observation.date'].dt.to_timestamp()

# Extract vaccination campaign start and end dates for plotting
vaccination_intervals['Campaign Start Date'] = pd.to_datetime(vaccination_intervals['Campaign Start Date'], errors='coerce')
vaccination_intervals['Campaign End Date'] = pd.to_datetime(vaccination_intervals['Campaign End Date'], errors='coerce')

# Plotting the comparative outbreak trends
plt.figure(figsize=(12, 6))
plt.plot(france_trends['Observation.date'], france_trends['Outbreaks'], label='France', marker='o')
plt.plot(europe_trends['Observation.date'], europe_trends['Outbreaks'], label='Europe (excluding France)', marker='x')

# Overlay vaccination campaigns
for _, row in vaccination_intervals.iterrows():
    plt.axvspan(row['Campaign Start Date'], row['Campaign End Date'] if pd.notnull(row['Campaign End Date']) else row['Campaign Start Date'],
                color='orange', alpha=0.3, label='Vaccination Campaign' if _ == 0 else "")

plt.title('Outbreak Trends with Vaccination Campaigns in France')
plt.xlabel('Date')
plt.ylabel('Number of Outbreaks')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
