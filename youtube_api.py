from googleapiclient.discovery import build
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

'''This code snippet uses the YouTube Data API to search for videos related to "Learning French".
Tt retrieves a maximum of 5 video results and prints the response.
Make sure to set the YOUTUBE_API_KEY environment variable before running this code.
'''

def setup_youtube_api():
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube = build(serviceName="youtube", version="v3", developerKey=YOUTUBE_API_KEY)
    return youtube

def search_youtube(youtube, query) -> str:
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=5
        )
        response = request.execute()

        results = []
        for item in response["items"]:
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            video_id = item["id"]["videoId"]
            print(f"{title} (https://www.youtube.com/watch?v={video_id})")
            results.append({
                "title": title,
                "description": description,
                "video_id": video_id
            })
        return str(results)

    except HttpError as e:
        s = "A YouTube API error occurred: " + e
        print(s)
        return s
    except Exception as e:
        s = "An error occurred: " + e
        return s

