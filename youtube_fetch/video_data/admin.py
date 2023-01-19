from django.contrib import admin
from video_data.models import YoutubeData

# Register your models here.


@admin.register(YoutubeData)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in YoutubeData._meta.get_fields()]
