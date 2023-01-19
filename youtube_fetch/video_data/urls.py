from django.urls import path
from video_data import views

urlpatterns = [
    path('search/', views.search_listing),
    path('', views.dashboard),
    # path('', views.get_latest_videos),
    # path('', views.LatestVideos.as_view()),
    # path('search/', views.SearchVideos.as_view())
]