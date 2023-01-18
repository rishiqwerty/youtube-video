from datetime import datetime
import os
import django
import requests
import json
from django.core.exceptions import MultipleObjectsReturned
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_fetch.settings")
django.setup()
from video_data.models import YoutubeData
from video_data.serializers import YoutubeDataSerializer
from celery import shared_task
# AIzaSyAIcZTxLObmbN5wY0TW4kW93NwNL14urrg
# AIzaSyDWFWe2slXJZnqbxXNNaN9byLswFIXiuQY
@shared_task()
def populate_db():
    api_key = 'AIzaSyCxucWHdXBlRZ8JXOnqGrMyl3FRGvbS2G8'
    url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&publishedAfter=2023-01-17T16%3A23%3A36Z&q=cricket&key={api_key}'

    response = requests.get(url)
    json_data = json.loads(response.text)['items']
    for data in json_data:
        vid_id = data.get('id')['videoId']
        video_title = data.get('snippet')['title']
        description = data.get('snippet')['description']
        publish_time = data.get('snippet')['publishTime']
        thumbnails = data.get('snippet')['thumbnails']
        vid_url = f'https://www.youtube.com/watch?v={vid_id}'
        channel_name = data.get('snippet')['channelTitle']
        channel_id = data.get('snippet')['channelId']
        
        try:
            vid_data = YoutubeData.objects.get(video_id=vid_id)
            print('Data already present')
        except MultipleObjectsReturned:
            print('Data already present')
        except:
            new_vid_data = YoutubeData(
                video_id = vid_id,
                video_title = video_title,
                description = description,
                published_time = publish_time,
                thumbnails = thumbnails,
                urls = vid_url,
                channel_name = channel_name,
                channel_id = channel_id,
                creation_time = datetime.now()
            )

            new_vid_data.save()
    
populate_db()