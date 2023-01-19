from django.urls import path
from video_data import views

urlpatterns = [
    path('search/', views.search_listing),
    path('', views.dashboard),
    path('rest/', views.LatestVideos.as_view()),
]