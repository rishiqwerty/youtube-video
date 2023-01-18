from datetime import timedelta
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_fetch.settings")
app = Celery("youtube_fetch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    ['db_populate_video_data']
)

app.conf.beat_schedule = {
    "video_data-task": {
        "task": "db_populate_video_data.populate_db",
        "schedule": timedelta(seconds=15),
    }
}
