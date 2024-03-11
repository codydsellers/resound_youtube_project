# YouTube Data Integration Project for Accounting Businesses

## Overview

This project automates the process of integrating YouTube data with a dataset of accounting businesses. It utilizes the YouTube Data API v3 to search for YouTube channels associated with these businesses, validates and cleans the URLs, extracts channel IDs, and finally fetches channel statistics and video details for these channels. The project consists of multiple Python scripts that perform specific tasks in the data integration process.

## Requirements

- Python 3.x
- Pandas library
- Google API Client library for Python
- A valid YouTube Data API v3 key

## Setup

1. **API Credentials**: Place your YouTube Data API v3 key in a `credentials.json` file in the project's root directory. The JSON file should have the following format:

    ```json
    {
      "api_key": "YOUR_API_KEY",
      "cse_id": "YOUR_CSE_ID" // Optional, only needed if using Custom Search Engine
    }
    ```

2. **Input Data**: Prepare a CSV file named `accounting_businesses.csv` with a list of accounting businesses. This file should be placed in the `input` directory. The CSV file must contain at least one column named `firm_name` with the names of the accounting firms.

## Components

The project is divided into several scripts, each handling different aspects of the data integration process:

1. **Initial Data Processing**: Searches YouTube channels for each accounting business, validates URLs, and extracts channel IDs. This step merges the newly obtained YouTube data with the original dataset.

2. **Channel Statistics**: Fetches statistics for each YouTube channel, such as subscriber count, view count, and video count. The script then updates the dataset with these statistics.

3. **Video Details Extraction**: For each channel, fetches details of its videos, including video ID, URL, title, and description. This data is saved as a separate CSV file.

## Output Files Description

This project generates several key output files, each serving a distinct purpose in the context of integrating YouTube data with the accounting businesses dataset. Below is a description of each output file and its contents:

1. **Accounting Businesses Updated with YouTube URLs (accounting_businesses_updated.csv)**: This CSV file contains the original dataset of accounting businesses, enriched with YouTube data. For each business, it includes the original information plus the following new columns:
   - `youtube_url`: The URL of the YouTube channel associated with the business.
   - `cleaned_youtube_url`: The YouTube URL after cleaning and validation.
   - `channel_id`: The unique identifier for the YouTube channel.

2. **Accounting Businesses with Channel Statistics (accounting_businesses_updated.csv)**: This is an updated version of the first output file, further enriched with statistics about each YouTube channel. The additional columns include:
   - `title`: The title of the YouTube channel.
   - `subscriberCount`: The number of subscribers to the channel.
   - `viewCount`: The total number of views across all videos on the channel.
   - `videoCount`: The total number of videos uploaded to the channel.

    Note: This file uses the same name as the initial output but replaces it with updated data, including channel statistics.

3. **Accounting Businesses YouTube Videos (accounting_businesses_youtube_videos.csv)**: This CSV file lists details of videos for the YouTube channels associated with the accounting businesses. Each row in this file represents a video, with columns for:
   - `BusinessName`: The name of the accounting business associated with the video.
   - `ChannelID`: The unique identifier of the YouTube channel.
   - `VideoID`: The unique identifier of the video.
   - `VideoURL`: The URL of the video on YouTube.
   - `VideoTitle`: The title of the video.
   - `VideoDescription`: The description of the video.

## Usage

- Execute each script in the order mentioned above, starting with the initial data processing script.
- Ensure the `credentials.json` file is correctly set up with your API key.
- The input CSV file should be ready in the `input` directory before running the scripts.
- Each script outputs its result to the `output` directory, which is used as input for the next script in the workflow.

## Important Notes

- The project incorporates delay between API calls to comply with YouTube's rate limit policies.
- Duplicate channel IDs are identified and handled to ensure data integrity.
- The final output consists of an updated dataset with YouTube channel statistics and a separate file listing details of videos from these channels.

## Conclusion

This Python project provides a streamlined approach to enriching a dataset of accounting businesses with relevant YouTube data, offering valuable insights into their digital presence. By automating the integration of YouTube channels, statistics, and video details, businesses can enhance their analysis and decision-making processes.