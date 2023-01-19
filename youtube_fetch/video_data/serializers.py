from rest_framework import serializers
from video_data.models import YoutubeData


class YoutubeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeData
        fields = '__all__'