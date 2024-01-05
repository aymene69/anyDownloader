from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("youtube_mp3/<str:id>", views.youtube_mp3, name="youtube_mp3"),
    path("youtube_mp4/<str:id>", views.youtube_mp4, name="youtube_mp4"),
]