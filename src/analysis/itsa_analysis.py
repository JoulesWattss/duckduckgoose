import statsmodels.api as sm
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
ANALYSIS_DIR = os.path.join(RESULTS_DIR, 'analysis')

# Define vaccination period
VACCINATION_START = pd.Timestamp('2023-10-01').tz_localize('UTC')
VACCINATION_END = pd.Timestamp('2024-10-01').tz_localize('UTC')

class ITSAnalysis:
    """
    Performs Interrupted Time Series Analysis on HPAI outbreak data.
    Includes data alignment and verification steps.
    """
    def __init__(self, france_monthly, control_monthly):
        """
        Initialize analysis with data alignment checks.
        """
        # First, ensure the data series are aligned
        self.align_data_series(france_monthly, control_monthly)
        
        # Create time variables for analysis
        self.time = np.arange(len(self.france_data))
        self.intervention = (self.france_data.index >= VACCINATION_START).astype(int)
        intervention_start_idx = np.where(self.france_data.index >= VACCINATION_START)[0][0]
        self.time_since_intervention = np.where(
            self.intervention,
            self.time - intervention_start_idx,
            0
        )
        
        # Print data verification
        print("\nData Verification:")
        print(f"Number of time points: {len(self.time)}")
        print(f"Date range: {self.france_data.index.min()} to {self.france_data.index.max()}")
        print(f"Intervention point: {VACCINATION_START}")

    def align_data_series(self, france_monthly, control_monthly):
        """
        Align the two data series to ensure they cover the same time period.
        """
        # Find common date range
        start_date = max(france_monthly.index.min(), control_monthly.index.min())
        end_date = min(france_monthly.index.max(), control_monthly.index.max())
        
        print("\nData Alignment:")
        print(f"Original date ranges:")
        print(f"France: {france_monthly.index.min()} to {france_monthly.index.max()}")
        print(f"Control: {control_monthly.index.min()} to {control_monthly.index.max()}")
        print(f"\nAligned date range: {start_date} to {end_date}")
        
        # Trim both series to common range
        self.france_data = france_monthly[start_date:end_date]
        self.control_data = control_monthly[start_date:end_date]
        
        # Verify alignment
        if len(self.france_data) != len(self.control_data):
            raise ValueError("Data series lengths don't match after alignment")
        
        print(f"Number of months in aligned series: {len(self.france_data)}")

    def perform_analysis(self):
        """
        Conducts the main statistical analysis with aligned data.
        """
        # Verify dimensions before analysis
        print("\nAnalysis Dimensions:")
        print(f"Design matrix shape: {len(self.time)} x 4")
        print(f"France data shape: {len(self.france_data)}")
        print(f"Control data shape: {len(self.control_data)}")
        
        # Prepare design matrix for regression
        X = np.column_stack([
            np.ones(len(self.time)),           # Intercept
            self.time,                         # Baseline trend
            self.intervention,                 # Level change
            self.time_since_intervention       # Slope change
        ])
        
        # Fit models
        france_model = sm.OLS(self.france_data.values, X).fit()
        control_model = sm.OLS(self.control_data.values, X).fit()
        
        # Calculate difference-in-differences
        did_effect = france_model.params[2] - control_model.params[2]
        
        return {
            'france_results': france_model,
            'control_results': control_model,
            'did_effect': did_effect
        }

    def create_analysis_visualizations(self):
        """
        Creates comprehensive visualizations showing the impact of vaccination.
        Includes trend lines, confidence intervals, and key statistics.
        """
        fig = plt.figure(figsize=(15, 10))
        
        # Create main time series plot
        ax = plt.subplot(111)
        
        # Plot raw data points
        ax.plot(self.france_data.index, self.france_data.values, 
                'b.', label='France (observed)', alpha=0.5)
        ax.plot(self.control_data.index, self.control_data.values, 
                'g.', label='Control (observed)', alpha=0.5)
        
        # Prepare design matrix for predictions
        X = np.column_stack([
            np.ones(len(self.time)),
            self.time,
            self.intervention,
            self.time_since_intervention
        ])
        
        # Fit models and get predictions
        france_model = sm.OLS(self.france_data.values, X).fit()
        control_model = sm.OLS(self.control_data.values, X).fit()
        
        # Add trend lines
        ax.plot(self.france_data.index, france_model.fittedvalues, 
                'b-', label='France (predicted)', linewidth=2)
        ax.plot(self.control_data.index, control_model.fittedvalues, 
                'g-', label='Control (predicted)', linewidth=2)
        
        # Add vaccination period shading
        ax.axvspan(VACCINATION_START, VACCINATION_END, 
                   color='yellow', alpha=0.2, label='Vaccination Period')
        
        # Calculate key statistics for annotation
        pre_vac_mask = self.france_data.index < VACCINATION_START
        during_vac_mask = (self.france_data.index >= VACCINATION_START) & (self.france_data.index < VACCINATION_END)
        
        reduction = ((self.france_data[pre_vac_mask].mean() - 
                     self.france_data[during_vac_mask].mean()) / 
                    self.france_data[pre_vac_mask].mean() * 100)
        
        # Add statistical annotations
        ax.text(0.02, 0.98, 
                f'Reduction in French outbreaks: {reduction:.1f}%\n' +
                f'p-value: {france_model.pvalues[2]:.4f}',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(facecolor='white', alpha=0.8))
        
        # Customize the plot
        ax.set_title('HPAI Outbreaks Over Time with Vaccination Impact', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Outbreaks', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        return fig

    def generate_statistical_report(self):
        """
        Generates a comprehensive statistical report of the analysis findings.
        """
        # Calculate statistics for each period
        pre_vac = self.france_data[self.france_data.index < VACCINATION_START]
        during_vac = self.france_data[(self.france_data.index >= VACCINATION_START) & 
                                    (self.france_data.index < VACCINATION_END)]
        post_vac = self.france_data[self.france_data.index >= VACCINATION_END]
        
        # Prepare report sections
        report = []
        report.append("HPAI Vaccination Impact Analysis Report")
        report.append("=====================================")
        
        report.append("\nPre-Vaccination Period Statistics:")
        report.append(f"Average monthly outbreaks: {pre_vac.mean():.2f}")
        report.append(f"Standard deviation: {pre_vac.std():.2f}")
        report.append(f"Number of months: {len(pre_vac)}")
        
        report.append("\nVaccination Period Statistics:")
        report.append(f"Average monthly outbreaks: {during_vac.mean():.2f}")
        report.append(f"Standard deviation: {during_vac.std():.2f}")
        report.append(f"Number of months: {len(during_vac)}")
        
        report.append("\nPost-Vaccination Period Statistics:")
        report.append(f"Average monthly outbreaks: {post_vac.mean():.2f}")
        report.append(f"Standard deviation: {post_vac.std():.2f}")
        report.append(f"Number of months: {len(post_vac)}")
        
        return "\n".join(report)

def main():
    """
    Main function to run the analysis with data loading and error checking.
    """
    try:
        # Create output directory
        os.makedirs(ANALYSIS_DIR, exist_ok=True)
        
        # Load data
        print("Loading data...")
        france_data = pd.read_csv(
            os.path.join(DATA_DIR, 'processed', 'france_hpai_outbreaks.csv'),
            parse_dates=['observation date']
        )
        control_data = pd.read_csv(
            os.path.join(DATA_DIR, 'processed', 'europe_control_group.csv'),
            parse_dates=['observation date']
        )
        
        # Ensure dates have UTC timezone
        if france_data['observation date'].dt.tz is None:
            france_data['observation date'] = france_data['observation date'].dt.tz_localize('UTC')
        if control_data['observation date'].dt.tz is None:
            control_data['observation date'] = control_data['observation date'].dt.tz_localize('UTC')
        
        # Prepare monthly data
        france_monthly = france_data.set_index('observation date').resample('ME').size()
        control_monthly = control_data.set_index('observation date').resample('ME').size()
        
        # Initialize and run analysis
        print("\nPerforming interrupted time series analysis...")
        analysis = ITSAnalysis(france_monthly, control_monthly)
        results = analysis.perform_analysis()
        
        # Generate visualizations
        print("\nCreating analysis visualizations...")
        fig = analysis.create_analysis_visualizations()
        fig.savefig(os.path.join(ANALYSIS_DIR, 'vaccination_impact.png'))
        plt.close(fig)
        
        # Generate and save statistical report
        print("\nGenerating statistical report...")
        report = analysis.generate_statistical_report()
        with open(os.path.join(ANALYSIS_DIR, 'statistical_report.txt'), 'w') as f:
            f.write(report)
        
        print("\nAnalysis complete! Results saved to:")
        print(f"- Visualization: {os.path.join(ANALYSIS_DIR, 'vaccination_impact.png')}")
        print(f"- Statistical Report: {os.path.join(ANALYSIS_DIR, 'statistical_report.txt')}")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script location: {SCRIPT_DIR}")
        print(f"Project root: {PROJECT_ROOT}")

if __name__ == "__main__":
    main()