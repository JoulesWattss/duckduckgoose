import matplotlib.pyplot as plt
import seaborn as sns

class ImpactVisualizer:
    def __init__(self, france_data, control_data, intervention_start):
        self.france_data = france_data
        self.control_data = control_data
        self.intervention_start = intervention_start
        plt.style.use('seaborn')

    def create_impact_dashboard(self, save_path):
        """
        Create a comprehensive dashboard of vaccination impact visualizations.
        """
        fig = plt.figure(figsize=(20, 15))
        
        # Main time series with intervention
        ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
        self._plot_main_series(ax1)
        
        # Pre-post boxplots
        ax2 = plt.subplot2grid((3, 2), (1, 0))
        self._plot_boxplots(ax2)
        
        # Seasonal patterns
        ax3 = plt.subplot2grid((3, 2), (1, 1))
        self._plot_seasonal_patterns(ax3)
        
        # Effect size comparison
        ax4 = plt.subplot2grid((3, 2), (2, 0))
        self._plot_effect_sizes(ax4)
        
        # Monthly variability
        ax5 = plt.subplot2grid((3, 2), (2, 1))
        self._plot_variability(ax5)
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    def _plot_main_series(self, ax):
        """Plot main time series with intervention line."""
        ax.plot(self.france_data.index, self.france_data.values, 
                label='France', color='blue')
        ax.plot(self.control_data.index, self.control_data.values, 
                label='Control Group', color='green')
        
        ax.axvline(self.intervention_start, color='red', linestyle='--', 
                   label='Vaccination Start')
        
        ax.set_title('HPAI Outbreaks Over Time', fontsize=12)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Outbreaks')
        ax.legend()

    def _plot_boxplots(self, ax):
        """Create pre-post comparison boxplots."""
        pre_mask = self.france_data.index < self.intervention_start
        
        data_to_plot = {
            'France Pre': self.france_data[pre_mask],
            'France Post': self.france_data[~pre_mask],
            'Control Pre': self.control_data[pre_mask],
            'Control Post': self.control_data[~pre_mask]
        }
        
        ax.boxplot(data_to_plot.values())
        ax.set_xticklabels(data_to_plot.keys(), rotation=45)
        ax.set_title('Distribution of Outbreaks Before and After Vaccination')
        ax.set_ylabel('Number of Outbreaks')
