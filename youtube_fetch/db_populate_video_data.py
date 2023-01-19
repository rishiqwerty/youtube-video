from celery import shared_task
from video_data.models import YoutubeData
from datetime import datetime, timedelta
import os
import django
import requests
import json
from django.core.exceptions import MultipleObjectsReturned

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_fetch.settings")
django.setup()

'''
    Celery task to populate db every minute
'''

@shared_task
def populate_db():
    api_key = [
        "AIzaSyAONpP4UI_tDPJ-jIjQvVkGuRkKVE2hggo",
        "AIzaSyDWFWe2slXJZnqbxXNNaN9byLswFIXiuQY",
        "AIzaSyDdYNrqSKO1xrcRdTIZZcQZP4Eu7LzKjiU",
        "AIzaSyDiAYnNh_0fJvfdYsr8BSH_ljf6IdRqXuk",
        "AIzaSyCU_U1fkBAjidh7-qUFMZHVCnhLKbyOe4I",
        "AIzaSyDDOOfn9R9wucx7-T5V5NPLyLvVfqg-pQI"
    ]
    # Added three API keys whichever will work will store data other wise it will throw daily limit reached error
    for api in api_key:
        date_to_fetch_from = str(datetime.today().date() - timedelta(days=2))
        url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&publishedAfter={date_to_fetch_from}T16%3A23%3A36Z&q=cricket&key={api}"

        response = requests.get(url)
        if response.status_code > 399:
            print("Api reached daily limit", response.status_code)
            continue
        print(response.status_code)
        json_data = json.loads(response.text)["items"]
        for data in json_data:
            vid_id = data.get("id")["videoId"]
            video_title = data.get("snippet")["title"]
            description = data.get("snippet")["description"]
            publish_time = data.get("snippet")["publishTime"]
            thumbnails = data.get("snippet")["thumbnails"]
            vid_url = f"https://www.youtube.com/watch?v={vid_id}"
            channel_name = data.get("snippet")["channelTitle"]
            channel_id = data.get("snippet")["channelId"]

            try:
                vid_data = YoutubeData.objects.get(video_id=vid_id)
                # print('Data already present')
            except MultipleObjectsReturned:
                pass
                # print('Data already present')
            except:
                new_vid_data = YoutubeData(
                    video_id=vid_id,
                    video_title=video_title,
                    description=description,
                    published_time=publish_time,
                    thumbnails=thumbnails,
                    urls=vid_url,
                    channel_name=channel_name,
                    channel_id=channel_id,
                    creation_time=datetime.now(),
                )

                new_vid_data.save()
        break
