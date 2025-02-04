import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import calendar
import os

# Get the absolute path to the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# The script is in src/visualization, so we need to go up two levels to reach the project root
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

# Define all required paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
FRANCE_DATA = os.path.join(PROJECT_ROOT, 'data', 'processed', 'france_hpai_outbreaks.csv')
CONTROL_DATA = os.path.join(PROJECT_ROOT, 'data', 'processed', 'europe_control_group.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'results', 'figures')

# vaccination period dates
VACCINATION_START = pd.Timestamp('2023-10-01')
VACCINATION_END = pd.Timestamp('2024-10-01')

def create_comparative_timeline_with_vaccination(france_monthly, control_monthly, save_path):
    """
    Create comparative timeline with vaccination period highlighted.
    """
    plt.figure(figsize=(15, 8))
    
    # Plot data
    plt.plot(france_monthly.index, france_monthly.values, 
             label='France', color='blue', linewidth=2)
    plt.plot(control_monthly.index, control_monthly.values, 
             label='Other European Countries', color='green', linewidth=2)
    
    # Add vaccination period highlighting
    plt.axvspan(VACCINATION_START, VACCINATION_END, 
                alpha=0.2, color='yellow', 
                label='French Vaccination Period')
    
    # Customize the plot
    plt.title('HPAI Outbreaks: France vs Other European Countries\nwith Vaccination Period', 
             fontsize=14, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Outbreaks', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_relative_change_plot(france_monthly, control_monthly, save_path=None):
    """
    Create a plot showing relative change with vaccination period highlighted,
    including careful handling of infinite values and outliers.
    """
    plt.figure(figsize=(15, 8))
    
    # Calculate month-over-month percentage changes
    france_pct_change = france_monthly.pct_change() * 100
    control_pct_change = control_monthly.pct_change() * 100
    
    # Replace infinite values with NaN
    france_pct_change = france_pct_change.replace([np.inf, -np.inf], np.nan)
    control_pct_change = control_pct_change.replace([np.inf, -np.inf], np.nan)
    
    # Calculate reasonable y-axis limits (excluding NaN values)
    all_changes = pd.concat([france_pct_change, control_pct_change])
    max_change = np.nanpercentile(all_changes, 95)  # 95th percentile
    min_change = np.nanpercentile(all_changes, 5)   # 5th percentile
    
    # Add some padding to the limits
    y_range = max_change - min_change
    max_change = max_change + (y_range * 0.1)
    min_change = min_change - (y_range * 0.1)
    
    # Plot percentage changes
    plt.plot(france_pct_change.index, france_pct_change.values, 
             label='France', color='blue')
    plt.plot(control_pct_change.index, control_pct_change.values, 
             label='Other European Countries', color='green')
    
    # Add zero line for reference
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add vaccination period highlighting
    plt.axvspan(VACCINATION_START, VACCINATION_END, 
                alpha=0.2, color='yellow', 
                label='French Vaccination Period')
    
    plt.title('Month-over-Month Percentage Change in HPAI Outbreaks\nwith Vaccination Period', 
             fontsize=14, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Percentage Change from Previous Month', fontsize=12)
    plt.legend(fontsize=10, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Set reasonable y-axis limits
    plt.ylim(min_change, max_change)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_rolling_average_comparison(france_monthly, control_monthly, window=3, save_path=None):
    """
    Create a plot showing rolling averages to smooth out short-term fluctuations.
    The rolling average helps identify underlying trends by reducing noise in the data.
    """
    plt.figure(figsize=(15, 8))
    
    # Calculate rolling averages with careful handling of NaN values
    france_rolling = france_monthly.rolling(window=window, min_periods=1).mean()
    control_rolling = control_monthly.rolling(window=window, min_periods=1).mean()
    
    # Plot both raw data (lighter) and rolling averages (darker)
    plt.plot(france_monthly.index, france_monthly.values, 
             alpha=0.3, color='blue', label='France (Raw)')
    plt.plot(france_rolling.index, france_rolling.values, 
             color='darkblue', label=f'France ({window}-Month Rolling Average)')
    
    plt.plot(control_monthly.index, control_monthly.values, 
             alpha=0.3, color='green', label='Control (Raw)')
    plt.plot(control_rolling.index, control_rolling.values, 
             color='darkgreen', label=f'Control ({window}-Month Rolling Average)')
    
    # Add vaccination period highlighting
    plt.axvspan(VACCINATION_START, VACCINATION_END, 
                alpha=0.2, color='yellow', 
                label='French Vaccination Period')
    
    plt.title(f'HPAI Outbreaks: {window}-Month Rolling Average Comparison\nwith Vaccination Period', 
             fontsize=14, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Outbreaks', fontsize=12)
    plt.legend(fontsize=10, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_outbreak_severity_boxplot(france_df, control_df, save_path=None):
    """
    Create boxplots comparing outbreak patterns between regions.
    The boxplot shows the distribution of monthly outbreak counts,
    helping identify typical ranges and outliers for each region.
    """
    plt.figure(figsize=(12, 6))
    
    # Prepare data for boxplot using the updated 'ME' frequency
    france_monthly_counts = france_df.groupby(
        pd.Grouper(key='observation date', freq='ME')).size()
    control_monthly_counts = control_df.groupby(
        pd.Grouper(key='observation date', freq='ME')).size()
    
    # Define colors for each box
    colors = ['blue', 'green']
    
    # Create box plot with custom colors
    bp = plt.boxplot([france_monthly_counts, control_monthly_counts],
                    tick_labels=['France', 'Other European Countries'],  # Updated parameter name
                    patch_artist=True)  # Enable filling of boxes with colors
    
    # Customize the appearance of the boxes
    for i, box in enumerate(bp['boxes']):
        box.set(facecolor=colors[i], alpha=0.7)  # Set box color and transparency
        plt.setp(bp['medians'][i], color='black')  # Make median lines black
        plt.setp(bp['fliers'][i], markerfacecolor=colors[i])  # Color the outlier points
        plt.setp(bp['whiskers'][2*i:2*i+2], color=colors[i])  # Color the whiskers
        plt.setp(bp['caps'][2*i:2*i+2], color=colors[i])  # Color the caps
    
    plt.title('Distribution of Monthly HPAI Outbreaks', fontsize=14, pad=20)
    plt.ylabel('Number of Outbreaks per Month', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    """
    Main function to generate all visualizations.
    """
    try:
        # Create output directory if it doesn't exist
        print(f"Creating output directory at: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Check if input files exist
        if not os.path.exists(FRANCE_DATA):
            raise FileNotFoundError(f"France data file not found at: {FRANCE_DATA}")
        if not os.path.exists(CONTROL_DATA):
            raise FileNotFoundError(f"Control data file not found at: {CONTROL_DATA}")
        
        # Load and prepare data
        print("Loading data files...")
        france_df = pd.read_csv(FRANCE_DATA, parse_dates=['observation date'])
        control_df = pd.read_csv(CONTROL_DATA, parse_dates=['observation date'])
        
        # Update resampling to use 'ME' (month end) instead of 'M'
        france_monthly = france_df.set_index('observation date').resample('ME').size()
        control_monthly = control_df.set_index('observation date').resample('ME').size()
        
        # Generate all visualizations
        create_comparative_timeline_with_vaccination(
            france_monthly, control_monthly,
            os.path.join(OUTPUT_DIR, 'comparative_timeline_with_vaccination.png'))
        print("Created comparative timeline")
        
        create_rolling_average_comparison(
            france_monthly, control_monthly,
            save_path=os.path.join(OUTPUT_DIR, 'rolling_average_comparison.png'))
        print("Created rolling average comparison with vaccination period")
        
        create_relative_change_plot(
            france_monthly, control_monthly,
            save_path=os.path.join(OUTPUT_DIR, 'relative_change.png'))
        print("Created relative change plot with vaccination period")
        
        create_outbreak_severity_boxplot(
            france_df, control_df,
            save_path=os.path.join(OUTPUT_DIR, 'outbreak_severity_boxplot.png'))
        print("Created outbreak severity boxplot")
        
        print("\nAll visualizations have been generated successfully!")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script location: {SCRIPT_DIR}")
        print(f"Project root: {PROJECT_ROOT}")
        print(f"Does France data exist? {os.path.exists(FRANCE_DATA)}")
        print(f"Does Control data exist? {os.path.exists(CONTROL_DATA)}")
        print(f"Does output directory exist? {os.path.exists(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()