from django.conf.urls.static import static
from django.urls import path, re_path, include
from rest_framework import routers

from music_app import settings
from . import views


router = routers.SimpleRouter()
router.register(r'tracks', views.TrackViewSet)
router.register(r'artists', views.ArtistViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),

    re_path(r'^media/audio/(?P<path>.+)$', views.ServeAudioView.as_view(), name='serve-audio')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
