from googleapiclient.discovery import build

# Function to search for YouTube channel
def search_youtube_channel(api_key, cse_id, business_name):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=f'{business_name} Youtube Channel', cx=cse_id).execute()
    for item in res.get('items', []):
        if 'youtube.com/channel' in item['link']:
            return item['link']  # Return the channel URL
    return None  # Return None if no channel is found

# Function to extract channel id from the url.
def extract_channel_id(url):
    if isinstance(url, str) and 'youtube.com/channel/' in url:
        # Split by "/channel/" and take the second element, then split by "/" again to avoid any additional paths
        return url.split('/channel/')[1].split('/')[0]
    return None

def validate_url_pattern(url):
    if any(x in url for x in ['youtube.com/@', 'youtube.com/c/', 'youtube.com/channel/']):
        return url
    else:
        return ''  # Clear the URL if it doesn't match the patterns

# Function to clean the URL
def clean_url(url):
    # Check if URL is a string and contains the expected pattern
    if isinstance(url, str) and 'youtube.com/channel/' in url:
        # Split by "/channel/" and take the second element, then split by "/" to avoid additional paths
        channel_id = url.split('/channel/')[1].split('/')[0]
        # Reconstruct the URL with just the channel ID
        return f'https://www.youtube.com/channel/{channel_id}'
    else:
        return url  # Return the original url if it doesn't match