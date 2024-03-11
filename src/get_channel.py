import pandas as pd
import time
import os
import sys
import json

# Add the functions directory to the sys.path to import the module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'functions'))
from get_channel_functions import search_youtube_channel, extract_channel_id, validate_url_pattern, clean_url

# Load API credentials from the JSON file in the root directory
root_dir = os.path.join(os.path.dirname(__file__), '..')
credentials_path = os.path.join(root_dir, 'credentials.json')
with open(credentials_path, 'r') as credentials_file:
    credentials = json.load(credentials_file)

api_key = credentials['api_key']
cse_id = credentials['cse_id']

# Load the list of businesses from the CSV file in the 'input' directory
input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
original_df = pd.read_csv(os.path.join(input_dir, 'accounting_businesses.csv'))

# Initialize a list to collect new YouTube URLs
youtube_data = []

# Iterate over the businesses
for count, firm_name in enumerate(original_df['firm_name'].unique(), start=1):
    # Use the API key and CSE ID from the credentials file
    youtube_url = search_youtube_channel(api_key, cse_id, firm_name)
    youtube_data.append({'firm_name': firm_name, 'youtube_url': youtube_url})
    time.sleep(0.25)  # Add a delay of 0.5 seconds between each API call
    print(f'Processed {count} records out of {len(original_df["firm_name"].unique())}')

# Convert the list of dictionaries into a DataFrame
youtube_df = pd.DataFrame(youtube_data)

# Apply the URL pattern validation and clean the URL
youtube_df['youtube_url'] = youtube_df['youtube_url'].apply(lambda x: validate_url_pattern(x) if pd.notnull(x) else x)
youtube_df['cleaned_youtube_url'] = youtube_df['youtube_url'].apply(clean_url)

# Extract channel ID from the cleaned YouTube URL
youtube_df['channel_id'] = youtube_df['cleaned_youtube_url'].apply(lambda x: extract_channel_id(x) if x != '' else None)

# Merge the new YouTube URL data into the original DataFrame
# Assuming 'firm_name' is the column to join on and it's unique
merged_df = pd.merge(original_df, youtube_df[['firm_name', 'cleaned_youtube_url', 'channel_id']], on='firm_name', how='left')

# Save the merged DataFrame to the 'output' directory without the index
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
merged_df.to_csv(os.path.join(output_dir, 'accounting_businesses_updated.csv'), index=False)