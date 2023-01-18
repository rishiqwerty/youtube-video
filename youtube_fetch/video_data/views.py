from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from video_data.models import YoutubeData
from video_data.serializers import YoutubeDataSerializer
from rest_framework.generics import ListAPIView

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

from django.core.paginator import Paginator
# @api_view(['GET', 'POST'])
# def get_latest_videos(request):

#     if request.method == 'GET':
#         snippets = YoutubeData.objects.all()
#         serializer = YoutubeDataSerializer(snippets, many=True)
#         return Response(serializer.data)

class LatestVideos(ListAPIView):
    queryset = YoutubeData.objects.all().order_by('-published_time')
    serializer_class = YoutubeDataSerializer
    filter_backends = [SearchFilter]
    search_fields = ['video_title', 'description']


def listing(request):
    q = request.GET.get('q')
    if q:
        queryset = YoutubeData.objects.filter(Q(video_title__contains=q) | Q(video_title__contains=q)).order_by('-published_time')
    else:
        queryset = YoutubeData.objects.all().order_by('-published_time')
    paginator = Paginator(queryset, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_videos.html', {'page_obj': page_obj, 'q':q})

class SearchVideos(APIView):
    renderer_classes = [TemplateHTMLRenderer] 
    template_name = 'all_videos.html'

    def get(self, request):
        if 'q' in request.GET:
            q = request.GET['q']
            youtube_data = YoutubeData.objects.filter(Q(video_title__contains=q) | Q(video_title__contains=q)).order_by('-published_time')
            serializer = YoutubeDataSerializer()
            return Response({'youtube_data': youtube_data})
        else:
            youtube_data = YoutubeData.objects.all().order_by('-published_time')
            return Response({'youtube_data': youtube_data})