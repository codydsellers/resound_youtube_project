import pandas as pd
import time
import json
import os
from googleapiclient.discovery import build


# Load API credentials from the JSON file in the root directory
root_dir = os.path.join(os.path.dirname(__file__), '..')
credentials_path = os.path.join(root_dir, 'credentials.json')
with open(credentials_path, 'r') as credentials_file:
    credentials = json.load(credentials_file)

api_key = credentials['api_key']

# Setup the YouTube API client
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)

# Load the list of businesses from the CSV file in the 'input' directory
input_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
df = pd.read_csv(os.path.join(input_dir, 'accounting_businesses_updated.csv'))

# Check for duplicate 'channel_id' and blank out 'cleaned_youtube_url' and 'channel_id' if duplicates are found
duplicates = df['channel_id'].duplicated(keep=False)  # Mark all duplicates as True
df.loc[duplicates, ['cleaned_youtube_url', 'channel_id']] = ''  # Blank out the duplicates

# You might want to filter only non-null and non-empty 'channel_id' after cleaning duplicates
filtered_df = df[df['channel_id'].notnull() & (df['channel_id'] != '')]

# Prepare a dictionary to hold our channel stats
channel_stats = {
    'channel_id': [],
    'title': [],
    'subscriberCount': [],
    'viewCount': [],
    'videoCount': []
}

# Function to fetch stats for a batch of channel IDs
def fetch_channel_stats(channel_ids):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=",".join(channel_ids)  # Join channel IDs into a comma-separated string
    )
    response = request.execute()

    for item in response.get('items', []):
        channel_id = item['id']
        channel_stats['channel_id'].append(channel_id)
        channel_stats['title'].append(item['snippet']['title'])
        channel_stats['subscriberCount'].append(item['statistics'].get('subscriberCount', 0))
        channel_stats['viewCount'].append(item['statistics'].get('viewCount', 0))
        channel_stats['videoCount'].append(item['statistics'].get('videoCount', 0))

# Loop through channel IDs in batches of 50
for i in range(0, len(filtered_df['channel_id']), 50):
    batch_channel_ids = filtered_df['channel_id'].iloc[i:i+50].tolist()
    fetch_channel_stats(batch_channel_ids)
    time.sleep(1)  # Sleep to avoid hitting rate limits
    print(f'Processed {i + len(batch_channel_ids)} records out of {len(filtered_df["channel_id"])}')


# Convert the channel stats into a DataFrame
stats_df = pd.DataFrame(channel_stats)

# Merge the new stats DataFrame with the original DataFrame on channel_id
merged_df = pd.merge(df, stats_df, on='channel_id', how='left')

# Save the merged DataFrame to the 'output' directory without the index
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')

# Save the merged DataFrame back to CSV, updating the original file
merged_df.to_csv(os.path.join(output_dir, 'accounting_businesses_updated.csv'), index=False)