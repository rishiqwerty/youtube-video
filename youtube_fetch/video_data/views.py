from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from video_data.models import YoutubeData
from video_data.serializers import YoutubeDataSerializer
from rest_framework.generics import ListAPIView

from rest_framework.filters import SearchFilter

from django.core.paginator import Paginator
from django.core.cache import cache


class LatestVideos(ListAPIView):
    """
    Rest API with pagination and search functionality
    """

    queryset = YoutubeData.objects.all().order_by("-published_time")
    serializer_class = YoutubeDataSerializer
    filter_backends = [SearchFilter]
    search_fields = ["video_title", "description"]


def search_listing(request):
    """
    Search view displays data in descending order and also we can search data here
    """

    q = request.GET.get("q")
    if q:
        data = cache.get(q)
        if not data:
            queryset = YoutubeData.objects.filter(
                Q(video_title__contains=q) | Q(description__contains=q)
            ).order_by("-published_time")
            cache.set(q, queryset, 50)
        else:
            queryset = data
    else:
        data = cache.get('data')
        if not data:
            queryset = YoutubeData.objects.all().order_by("-published_time")
            cache.set('data', queryset, 10)
        else:
            queryset = data
    paginator = Paginator(queryset, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "all_videos.html", {"page_obj": page_obj, "q": q})


def dashboard(request):
    """
    This is home page here we can see the sorted data either descending ordered or ascending
    """

    sort = request.GET.get("sort")
    vid_title = request.GET.get("name_filter")
    channel = request.GET.get("channel_filter")
    if sort:
        if vid_title or channel:
            queryset = YoutubeData.objects.filter(
                Q(video_title__contains=vid_title) | Q(
                    channel_nname__contains=channel)
            ).order_by(sort)
        else:
            queryset = YoutubeData.objects.all().order_by(sort)
    else:
        if vid_title or channel:
            queryset = YoutubeData.objects.filter(
                Q(video_title__contains=vid_title) | Q(
                    channel_name__contains=channel)
            ).order_by("-published_time")
        else:
            queryset = YoutubeData.objects.all().order_by("-published_time")

    paginator = Paginator(queryset, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "dashboard.html", {"page_obj": page_obj, "sort": sort})
