from scipy.stats import ttest_ind, pearsonr
import pandas as pd


# Load the datasets
france_data = pd.read_csv('//filtered_france_data.csv')
bird_outbreaks = pd.read_csv('//bird_outbreaks.csv')
vaccination_intervals = pd.read_csv('//duck_vaccination_intervals.csv')

# Filter bird_outbreaks to exclude France
bird_outbreaks_europe = bird_outbreaks[bird_outbreaks['Country'] != 'France']

# Preprocess dates and aggregate outbreak counts for France and Europe
france_data['Observation.date'] = pd.to_datetime(france_data['Observation.date..dd.mm.yyyy.'], errors='coerce')
bird_outbreaks_europe['Observation.date'] = pd.to_datetime(bird_outbreaks_europe['Observation.date..dd.mm.yyyy.'], errors='coerce')

# Group data by month and count events
france_trends = france_data.groupby(france_data['Observation.date'].dt.to_period('M')).size().reset_index(name='Outbreaks')
europe_trends = bird_outbreaks_europe.groupby(bird_outbreaks_europe['Observation.date'].dt.to_period('M')).size().reset_index(name='Outbreaks')

# Align time series by common dates for comparison
common_dates = set(france_trends['Observation.date']).intersection(europe_trends['Observation.date'])
france_common = france_trends[france_trends['Observation.date'].isin(common_dates)]
europe_common = europe_trends[europe_trends['Observation.date'].isin(common_dates)]

# Perform t-test on outbreak counts
t_stat, p_value = ttest_ind(france_common['Outbreaks'], europe_common['Outbreaks'], equal_var=False)

# Correlation analysis between France's and Europe's outbreaks
correlation_value = pearsonr(france_common['Outbreaks'], europe_common['Outbreaks'])[0]

# Analyze pre- and post-vaccination effects in France
vaccination_intervals['Campaign Start Date'] = pd.to_datetime(vaccination_intervals['Campaign Start Date'], errors='coerce')
vaccination_intervals['Campaign End Date'] = pd.to_datetime(vaccination_intervals['Campaign End Date'], errors='coerce')

vaccination_periods = [
    france_common[(france_common['Observation.date'] >= row['Campaign Start Date']) &
                  (france_common['Observation.date'] <= row['Campaign End Date'])]
    for _, row in vaccination_intervals.iterrows()
]

if vaccination_periods:
    combined_vaccination_periods = pd.concat(vaccination_periods, ignore_index=True)
    post_vaccine_effects = combined_vaccination_periods['Outbreaks'].mean()
else:
    post_vaccine_effects = None

pre_vaccine_effects = france_common[~france_common['Observation.date'].isin(
    combined_vaccination_periods['Observation.date'] if vaccination_periods else []
)]['Outbreaks'].mean()

# Output statistical results
statistical_results = {
    "t-test": {"t-statistic": t_stat, "p-value": p_value},
    "correlation": correlation_value,
    "pre-vaccine mean outbreaks": pre_vaccine_effects,
    "post-vaccine mean outbreaks": post_vaccine_effects
}

print("Statistical Analysis Results:")
for key, value in statistical_results.items():
    print(f"{key}: {value}")
