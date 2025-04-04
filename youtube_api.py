from googleapiclient.discovery import build
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

'''This code snippet uses the YouTube Data API to search for videos related to "Learning French".
Tt retrieves a maximum of 5 video results and prints the response.
Make sure to set the YOUTUBE_API_KEY environment variable before running this code.
'''

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build(serviceName="youtube", version="v3", developerKey=YOUTUBE_API_KEY)

try:
    request = youtube.search().list(
        part="snippet",
        q="study French|C1|conversation|podcast",
        type="video",
        maxResults=5
    )
    response = request.execute()

    for item in response["items"]:
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        video_id = item["id"]["videoId"]
        print(f"{title} (https://www.youtube.com/watch?v={video_id})")

except HttpError as e:
    print("A YouTube API error occurred:", e)
except Exception as e:
    print("An error occurred:", e)

