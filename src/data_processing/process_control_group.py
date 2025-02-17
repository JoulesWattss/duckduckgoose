import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

# Define paths relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'raw', 'europe_hpai_bird_outbreaks.csv')
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'processed', 'europe_control_group.csv')
OUTPUT_JSON = os.path.join(PROJECT_ROOT, 'data', 'processed', 'europe_control_group_monthly.json')

def process_control_group(input_file, output_file):
    """
    Process European HPAI outbreak data excluding France to create control group dataset.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Could not find input file at: {input_file}")
    
    print(f"Reading data from: {input_file}")
    df = pd.read_csv(input_file, parse_dates=['observation date', 'report date'])
    
    # remove French data to create control group
    print("Creating control group by excluding French data...")
    control_df = df[df['Country'] != 'France'].copy()
    
    # sort chronologically
    print("Sorting by observation date...")
    control_df = control_df.sort_values('observation date')
    
    # add useful analytical fields
    print("Adding analytical fields...")
    
    # calculate days since first outbreak for to align outbreaks on consistent timeline
    first_outbreak = control_df['observation date'].min()
    control_df['days_since_first_outbreak'] = (
        control_df['observation date'] - first_outbreak).dt.days
    
    # add month-year field for monthly aggregation trend analysis
    control_df['month_year'] = control_df['observation date'].dt.to_period('M')
    
    # outbreaks by country
    country_counts = control_df['Country'].value_counts()
    control_df['country_total_outbreaks'] = control_df['Country'].map(country_counts)
    
    # reset index for clean sequential numbering
    control_df = control_df.reset_index(drop=True)
    
    # create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # save processed data
    print(f"Saving processed control group data to: {output_file}")
    control_df.to_csv(output_file, index=False)
    
    return control_df

def group_and_convert_to_json(df, json_output_path):
    """
    Groups the control group HPAI data by month and converts to JSON format
    """
    print("\nStarting monthly grouping process...")
    
    # Convert observation date to month-year format and group
    df['month_year'] = df['observation date'].dt.strftime('%Y-%m')
    monthly_counts = df.groupby('month_year').size().reset_index()
    monthly_counts.columns = ['month', 'outbreak_count']
    
    # Sort by date
    monthly_counts = monthly_counts.sort_values('month')
    
    # Convert to JSON format
    json_data = monthly_counts.to_dict('records')
    
    # Create output directory if it doesn't exist
    print(f"Creating directory: {os.path.dirname(json_output_path)}")
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    
    # Save to JSON file
    print(f"Saving JSON to: {json_output_path}")
    with open(json_output_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    
    print("JSON file has been created successfully")
    return json_data

def print_control_group_summary(control_df):
    """
    Print summary statistics for the control group data.
    """
    print("\nControl Group Summary:")
    print(f"Total non-French outbreaks: {len(control_df)}")
    print(f"\nDate range:")
    print(f"First outbreak: {control_df['observation date'].min()}")
    print(f"Last outbreak: {control_df['observation date'].max()}")
    
    print("\nOutbreaks by country:")
    country_summary = control_df.groupby('Country').size().sort_values(ascending=False)
    for country, count in country_summary.items():
        print(f"{country}: {count}")
    
    print("\nMonthly outbreak counts:")
    monthly_counts = control_df.groupby('month_year').size()
    print(monthly_counts)

if __name__ == "__main__":
    try:
        # Process control group data
        print("Processing control group data...")
        control_data = process_control_group(INPUT_FILE, OUTPUT_CSV)
        
        # Generate monthly JSON data
        print("\nGenerating monthly JSON data...")
        monthly_data = group_and_convert_to_json(control_data, OUTPUT_JSON)
        
        # Print detailed summary
        print_control_group_summary(control_data)
        
        # Print sample of monthly data
        print("\nSample of monthly grouped data (first 3 months):")
        print(json.dumps(monthly_data[:3], indent=2))
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"\nDebug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Input file path: {INPUT_FILE}")
        print(f"Does input file exist? {os.path.exists(INPUT_FILE)}")
        print(f"Output CSV exists? {os.path.exists(OUTPUT_CSV)}")
        print(f"Output JSON directory exists? {os.path.exists(os.path.dirname(OUTPUT_JSON))}")
        
# import pandas as pd
# import numpy as np
# from datetime import datetime
# import os
# import json

# # Define paths relative to project root
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'raw', 'europe_hpai_bird_outbreaks.csv')
# OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'processed', 'europe_control_group.csv')

# def process_control_group(input_file, output_file):
#     """
#     Process European HPAI outbreak data excluding France to create control group dataset.
    
#     """
    
#     if not os.path.exists(input_file):
#         raise FileNotFoundError(f"Could not find input file at: {input_file}")
    
#     print(f"Reading data from: {input_file}")
#     df = pd.read_csv(input_file, parse_dates=['observation date', 'report date'])
    
#     # remove French data to create control group
#     print("Creating control group by excluding French data...")
#     control_df = df[df['Country'] != 'France'].copy()
    
#     # sort chronologically
#     print("Sorting by observation date...")
#     control_df = control_df.sort_values('observation date')
    
#     # add useful analytical fields
#     print("Adding analytical fields...")
    
#     # calculate days since first outbreak for to align outbreaks on consistent timeline
#     first_outbreak = control_df['observation date'].min()
#     control_df['days_since_first_outbreak'] = (
#         control_df['observation date'] - first_outbreak).dt.days
    
#     # add month-year field for monthly aggregation trend analysis
#     control_df['month_year'] = control_df['observation date'].dt.to_period('M')
    
#     # outbreaks by country
#     country_counts = control_df['Country'].value_counts()
#     control_df['country_total_outbreaks'] = control_df['Country'].map(country_counts)
    
#     # reset index for clean sequential numbering
#     control_df = control_df.reset_index(drop=True)
    
#     # create the output directory if it doesn't exist
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
#     # save processed data
#     print(f"Saving processed control group data to: {output_file}")
#     control_df.to_csv(output_file, index=False)
    
#     return control_df

# def print_control_group_summary(control_df):
#     """
#     Print summary statistics for the control group data.
    
#     Parameters:
#     -----------
#     control_df : pd.DataFrame
#         Processed control group DataFrame
#     """
    
#     print("\nControl Group Summary:")
#     # print total oubreaks in the control group
#     print(f"Total non-French outbreaks: {len(control_df)}") 

#     # print date range of outbreaks
#     print(f"\nDate range:")

#     # print distribution of outbreaks across conutries
#     print(f"First outbreak: {control_df['observation date'].min()}")

#     # print monthly patterns for temporal trend analysis
#     print(f"Last outbreak: {control_df['observation date'].max()}")
    
#     print("\nOutbreaks by country:")
#     country_summary = control_df.groupby('Country').size().sort_values(ascending=False)
#     for country, count in country_summary.items():
#         print(f"{country}: {count}")
    
#     print("\nMonthly outbreak counts:")
#     monthly_counts = control_df.groupby('month_year').size()
#     print(monthly_counts)

# def group_and_convert_to_json(df, json_output_path):
#     """
#     Groups the French HPAI data by month and converts to JSON format
#     """
#     print("Starting monthly grouping process...")
    
#     # Convert observation date to month-year format and group
#     df['month_year'] = df['observation date'].dt.strftime('%Y-%m')
#     monthly_counts = df.groupby('month_year').size().reset_index()
#     monthly_counts.columns = ['month', 'outbreak_count']
    
#     # Sort by date
#     monthly_counts = monthly_counts.sort_values('month')
    
#     # Convert to JSON format
#     json_data = monthly_counts.to_dict('records')
    
#     print(f"Creating directory: {os.path.dirname(json_output_path)}")
#     os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
    
#     print(f"Saving JSON to: {json_output_path}")
#     with open(json_output_path, 'w') as f:
#         json.dump(json_data, f, indent=4)
    
#     print("JSON file has been created successfully")
#     return json_data

# if __name__ == "__main__":
#     try:
#         # Process control group data
#         control_data = process_control_group(INPUT_FILE, OUTPUT_FILE)
        
#         # Print detailed summary
#         print_control_group_summary(control_data)
        
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         print(f"\nDebug information:")
#         print(f"Current working directory: {os.getcwd()}")
#         print(f"Input file path: {INPUT_FILE}")
#         print(f"Does input file exist? {os.path.exists(INPUT_FILE)}")