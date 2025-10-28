from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from music_app import settings
from . import views
from .views import TrackAPIView

urlpatterns = [
    path('api/v1/tracks/', TrackAPIView.as_view()),
    path('api/v1/tracks/<slug:slug>', views.TrackDetailAPIView.as_view()),
    re_path(r'^media/audio/(?P<path>.+)$', views.ServeAudioView.as_view(), name='serve-audio')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
