from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_fetch.settings")
app = Celery("youtube_fetch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    ['db_populate_video_data']
)

app.conf.beat_schedule = {
    "populate_db": {
        "task": "db_populate_video_data.populate_db",
        # "schedule": 20.0
        "schedule": 60.0
    }
}
