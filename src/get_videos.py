import pandas as pd
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import time
import os

# Load API credentials from the JSON file in the root directory
root_dir = os.path.join(os.path.dirname(__file__), '..')
credentials_path = os.path.join(root_dir, 'credentials.json')
with open(credentials_path, 'r') as credentials_file:
    credentials = json.load(credentials_file)

api_key = credentials['api_key']

# Replace 'YOUR_API_KEY' with your actual YouTube Data API v3 key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Load the list of businesses from the CSV file in the 'input' directory
input_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
df = pd.read_csv(os.path.join(input_dir, 'accounting_businesses_updated.csv'))
filtered_df = df[df['channel_id'].notnull() & (df['channel_id'] != '')]

def youtube_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)

def get_channel_videos(channel_id):
    youtube = youtube_service()
    results = []
    try:
        request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, type="video")
        response = request.execute()

        for item in response.get('items', []):
            video_id = item['id']['videoId']
            video_details = youtube.videos().list(part='snippet', id=video_id).execute()
            for detail in video_details['items']:
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_title = detail['snippet']['title']
                video_description = detail['snippet']['description']
                results.append((video_id, video_url, video_title, video_description))
                time.sleep(0.1)  # Add a delay of 0.05 seconds between each API call
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')
    return results


videos_data = []
for _, row in filtered_df.iterrows():
    business_name = row['firm_name']
    channel_id = row['channel_id']
    videos = get_channel_videos(channel_id)
    for video_id, video_url, video_title, video_description in videos:
        videos_data.append([business_name, channel_id, video_id, video_url, video_title, video_description])

# Save the merged DataFrame to the 'output' directory without the index
videos_df = pd.DataFrame(videos_data, columns=['BusinessName', 'ChannelID', 'VideoID', 'VideoURL', 'VideoTitle', 'VideoDescription'])

output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')

videos_df.to_csv(os.path.join(output_dir, 'accounting_businesses_youtube_videos.csv'), index=False)
