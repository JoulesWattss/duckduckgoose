import pandas as pd
from datetime import datetime
import os
import json

# Define project root and paths - using your actual path structure
PROJECT_ROOT = "/Users/juliettewilliamson/Desktop/duckduckgoose_code"
INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'raw', 'europe_hpai_bird_outbreaks.csv')
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'processed', 'france_hpai_outbreaks.csv')
OUTPUT_JSON = os.path.join(PROJECT_ROOT, 'data', 'processed', 'france_hpai_outbreaks_monthly.json')

def extract_french_data(input_file, output_file):
    """
    Function to extract and process French HPAI outbreak data from broader European dataset.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Could not find input file at: {input_file}")
    
    print(f"Reading data from: {input_file}")
    df = pd.read_csv(input_file, parse_dates=['observation date', 'report date'])
    
    print("Filtering French data...")
    france_df = df[df['Country'] == 'France'].copy()
    
    print("Sorting by observation date...")
    france_df = france_df.sort_values('observation date')
    france_df = france_df.reset_index(drop=True)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Saving processed data to: {output_file}")
    france_df.to_csv(output_file, index=False)
    
    return france_df

def group_and_convert_to_json(df, json_output_path):
    """
    Groups the French HPAI data by month and converts to JSON format
    """
    print("Starting monthly grouping process...")
    
    # Convert observation date to month-year format and group
    df['month_year'] = df['observation date'].dt.strftime('%Y-%m')
    monthly_counts = df.groupby('month_year').size().reset_index()
    monthly_counts.columns = ['month', 'outbreak_count']
    
    # Sort by date
    monthly_counts = monthly_counts.sort_values('month')
    
    # Convert to JSON format
    json_data = monthly_counts.to_dict('records')
    
    print(f"Creating directory: {os.path.dirname(json_output_path)}")
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    
    print(f"Saving JSON to: {json_output_path}")
    with open(json_output_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    
    print("JSON file has been created successfully")
    return json_data

if __name__ == "__main__":
    try:
        # Extract and process French data
        print("Starting data extraction...")
        france_data = extract_french_data(INPUT_FILE, OUTPUT_CSV)
        
        # Group by month and convert to JSON
        print("\nStarting JSON conversion...")
        monthly_data = group_and_convert_to_json(france_data, OUTPUT_JSON)
        
        # Print summary statistics
        print("\nData Summary:")
        print(f"Total French outbreaks: {len(france_data)}")
        print("\nDate range:")
        print(f"First outbreak: {france_data['observation date'].min()}")
        print(f"Last outbreak: {france_data['observation date'].max()}")
        
        # Print sample of monthly data
        print("\nSample of monthly grouped data:")
        print(monthly_data[:3])
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Input file exists?: {os.path.exists(INPUT_FILE)}")
        print(f"Output CSV exists?: {os.path.exists(OUTPUT_CSV)}")
        print(f"Output JSON directory exists?: {os.path.exists(os.path.dirname(OUTPUT_JSON))}")
