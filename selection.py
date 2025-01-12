import pandas as pd

'''
First generate a file that keeps only the top 5 bird species
'''

# Load the CSV file
data_path = '/Users/juliettewilliamson/Desktop/going_viral/code/europe_outbreaks.csv'
data = pd.read_csv(data_path)

# Define the species to keep
species_to_keep = ["Duck", "Unspecified bird", "Goose", "Chicken", "Turkey"]

# Filter the DataFrame
data_filtered = data[data['Species'].isin(species_to_keep)]

# Display the filtered DataFrame
data_filtered.head()

# Optionally, save the filtered DataFrame to a new CSV file
filtered_path = '/Users/juliettewilliamson/Desktop/going_viral/code/bird_outbreaks.csv'
data_filtered.to_csv(filtered_path, index=False)


'''
Then generate a separate CSV file for French bird outbreak data based on updated file
'''

# Load the CSV file
data_path = '/Users/juliettewilliamson/Desktop/going_viral/code/bird_outbreaks.csv'
data = pd.read_csv(data_path)

# Define the species to keep
country = ["France"]

# Filter the DataFrame
data_filtered = data[data['Country'].isin(country)]

# Display the filtered DataFrame
data_filtered.head()

# Optionally, save the filtered DataFrame to a new CSV file
filtered_path = '/Users/juliettewilliamson/Desktop/going_viral/code/france_outbreaks.csv'
data_filtered.to_csv(filtered_path, index=False)





import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define a mapping of countries to regions
region_mapping = {
    'France': 'Western Europe',
    'Germany': 'Western Europe',
    'Italy': 'Southern Europe',
    'Spain': 'Southern Europe',
    'Poland': 'Eastern Europe',
    'Romania': 'Eastern Europe',
    'Greece': 'Southern Europe',
    'Netherlands': 'Western Europe',
    'Belgium': 'Western Europe',
    'Czech Republic': 'Eastern Europe',
    # Add more countries and their regions as needed
}

