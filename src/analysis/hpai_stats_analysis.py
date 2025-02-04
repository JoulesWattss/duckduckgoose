import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Define paths using the same structure as your visualization script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
OUTPUT_DIR = os.path.join(RESULTS_DIR, 'analysis')

VACCINATION_START = pd.Timestamp('2023-10-01').tz_localize('UTC')
VACCINATION_END = pd.Timestamp('2024-10-01').tz_localize('UTC')

class OutbreakAnalysis:
    def __init__(self, france_data_path, control_data_path):
        """Initialize the analysis with data paths and load the data."""
        # Read the data
        self.france_df = pd.read_csv(france_data_path, parse_dates=['observation date'])
        self.control_df = pd.read_csv(control_data_path, parse_dates=['observation date'])
        
        # Ensure observation dates have UTC timezone
        if self.france_df['observation date'].dt.tz is None:
            self.france_df['observation date'] = self.france_df['observation date'].dt.tz_localize('UTC')
        if self.control_df['observation date'].dt.tz is None:
            self.control_df['observation date'] = self.control_df['observation date'].dt.tz_localize('UTC')
        
        # Create monthly aggregations
        self.france_monthly = self.france_df.set_index('observation date').resample('ME').size()
        self.control_monthly = self.control_df.set_index('observation date').resample('ME').size()
        
        # Find the overlapping date range
        start_date = max(self.france_monthly.index.min(), self.control_monthly.index.min())
        end_date = min(self.france_monthly.index.max(), self.control_monthly.index.max())
        
        # Print date ranges for verification
        print("\nData coverage periods:")
        print(f"France data: {self.france_monthly.index.min()} to {self.france_monthly.index.max()}")
        print(f"Control data: {self.control_monthly.index.min()} to {self.control_monthly.index.max()}")
        print(f"\nAnalysis period (overlapping dates): {start_date} to {end_date}")
        
        # Trim both datasets to the overlapping period
        self.france_monthly = self.france_monthly[start_date:end_date]
        self.control_monthly = self.control_monthly[start_date:end_date]
        
        # Verify the lengths match
        print(f"\nNumber of months in analysis:")
        print(f"France data points: {len(self.france_monthly)}")
        print(f"Control data points: {len(self.control_monthly)}")
        
        # Create period masks for the aligned data
        self.pre_vac_mask = self.france_monthly.index < VACCINATION_START
        self.vac_mask = (self.france_monthly.index >= VACCINATION_START) & (self.france_monthly.index < VACCINATION_END)
        self.post_vac_mask = self.france_monthly.index >= VACCINATION_END
        
        # Print period coverage
        print("\nPeriod coverage:")
        print(f"Pre-vaccination months: {sum(self.pre_vac_mask)}")
        print(f"Vaccination period months: {sum(self.vac_mask)}")
        print(f"Post-vaccination months: {sum(self.post_vac_mask)}")


    def calculate_period_statistics(self):
        """Calculate key statistics for each period."""
        periods = ['Pre-Vaccination', 'Vaccination', 'Post-Vaccination']
        masks = [self.pre_vac_mask, self.vac_mask, self.post_vac_mask]
        
        stats_dict = {}
        for period, mask in zip(periods, masks):
            france_stats = {
                'mean': self.france_monthly[mask].mean(),
                'median': self.france_monthly[mask].median(),
                'std': self.france_monthly[mask].std(),
                'total': self.france_monthly[mask].sum(),
                'months': len(self.france_monthly[mask])
            }
            
            control_stats = {
                'mean': self.control_monthly[mask].mean(),
                'median': self.control_monthly[mask].median(),
                'std': self.control_monthly[mask].std(),
                'total': self.control_monthly[mask].sum(),
                'months': len(self.control_monthly[mask])
            }
            
            stats_dict[period] = {
                'France': france_stats,
                'Control': control_stats
            }
        
        return pd.DataFrame.from_dict({(i,j): stats_dict[i][j] 
                                     for i in stats_dict.keys() 
                                     for j in stats_dict[i].keys()},
                                     orient='index')

    def perform_statistical_tests(self):
        """Perform statistical tests to compare periods and regions."""
        # Compare France before and during vaccination
        france_before = self.france_monthly[self.pre_vac_mask]
        france_during = self.france_monthly[self.vac_mask]
        
        # Mann-Whitney U test (non-parametric test for comparing distributions)
        statistic, pvalue = stats.mannwhitneyu(
            france_before, france_during, alternative='two-sided')
        
        # Calculate effect size (Cohen's d)
        d = (france_during.mean() - france_before.mean()) / np.sqrt(
            (france_during.std()**2 + france_before.std()**2) / 2)
        
        return {
            'test_statistic': statistic,
            'p_value': pvalue,
            'effect_size': d
        }

    def analyze_seasonal_patterns(self):
        """Analyze seasonal patterns before and during vaccination."""
        # Create month-based averages for each period
        def get_monthly_averages(data, mask):
            period_data = data[mask]
            return period_data.groupby(period_data.index.month).mean()
        
        seasonal_patterns = {
            'Pre-Vaccination': {
                'France': get_monthly_averages(self.france_monthly, self.pre_vac_mask),
                'Control': get_monthly_averages(self.control_monthly, self.pre_vac_mask)
            },
            'Vaccination': {
                'France': get_monthly_averages(self.france_monthly, self.vac_mask),
                'Control': get_monthly_averages(self.control_monthly, self.vac_mask)
            }
        }
        
        return seasonal_patterns

    def create_seasonal_comparison_plot(self, save_path=None):
        """Create a plot comparing seasonal patterns before and during vaccination."""
        seasonal_data = self.analyze_seasonal_patterns()
        
        plt.figure(figsize=(15, 8))
        months = range(1, 13)
        
        # Plot pre-vaccination patterns
        plt.plot(months, seasonal_data['Pre-Vaccination']['France'], 
                'b--', label='France (Pre-Vaccination)')
        plt.plot(months, seasonal_data['Pre-Vaccination']['Control'], 
                'g--', label='Control (Pre-Vaccination)')
        
        # Plot vaccination period patterns
        plt.plot(months, seasonal_data['Vaccination']['France'], 
                'b-', label='France (During Vaccination)')
        plt.plot(months, seasonal_data['Vaccination']['Control'], 
                'g-', label='Control (During Vaccination)')
        
        plt.title('Seasonal Patterns of HPAI Outbreaks\nBefore and During Vaccination', 
                 fontsize=14, pad=20)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Number of Outbreaks', fontsize=12)
        plt.xticks(months, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
        plt.close()

def main():
    """Run the complete analysis and save results."""
    try:
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        print("\nInitializing analysis...")
        analysis = OutbreakAnalysis(
            os.path.join(DATA_DIR, 'processed', 'france_hpai_outbreaks.csv'),
            os.path.join(DATA_DIR, 'processed', 'europe_control_group.csv')
        )
        
        print("\nCalculating period statistics...")
        stats_df = analysis.calculate_period_statistics()
        stats_path = os.path.join(OUTPUT_DIR, 'period_statistics.csv')
        stats_df.to_csv(stats_path)
        print(f"Statistics saved to: {stats_path}")
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script location: {SCRIPT_DIR}")
        print(f"Project root: {PROJECT_ROOT}")
        print(f"Does output directory exist? {os.path.exists(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()