import pandas as pd
from datetime import datetime
import os

# defining paths to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'raw', 'europe_hpai_bird_outbreaks.csv')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'processed', 'france_hpai_outbreaks.csv')

def extract_french_data(input_file, output_file):
    """
    Function to extract and process French HPAI outbreak data from broader European dataset.
    Parameters == str paths to CSV files (input is European data, output is where French data will be stored)
    Returns: pd.DataFrame containing only French outbreak data 
    """
    
    # verifying the existence of the input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Could not find input file at: {input_file}")
    
    # parse_dates for future temporal analysis
    print(f"Reading data from: {input_file}")
    df = pd.read_csv(input_file, parse_dates=['observation date', 'report date'])
    
    # filter european data for France exclusively
    print("Filtering French data...")
    france_df = df[df['Country'] == 'France'].copy()
    
    # sort filtered data by date
    print("Sorting by observation date...")
    france_df = france_df.sort_values('observation date')
    france_df = france_df.reset_index(drop=True)
    
    # create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # save processed data
    print(f"Saving processed data to: {output_file}")
    france_df.to_csv(output_file, index=False)
    
    return france_df

if __name__ == "__main__":
    try:
        france_data = extract_french_data(INPUT_FILE, OUTPUT_FILE)
        
        # printing summary statistics for verification
        print("\nData Summary:")
        print(f"Total French outbreaks: {len(france_data)}")
        print("\nDate range:")
        print(f"First outbreak: {france_data['observation date'].min()}")
        print(f"Last outbreak: {france_data['observation date'].max()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Input file path: {INPUT_FILE}")
        print(f"Does input file exist? {os.path.exists(INPUT_FILE)}")




