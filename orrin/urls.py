from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from rest_framework import routers

from orrin import views

router = routers.SimpleRouter()
router.register(r'tracks', views.TrackViewSet)
router.register(r'artists', views.ArtistViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('library/playlists/', views.PlaylistListView.as_view(), name='playlist-list'),
    path('library/playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('library/playlists/<int:pk>/tracks/', views.PlaylistTrackView.as_view(), name='playlist-tracks'),
    path('library/playlists/<int:pk>/tracks/<slug:track_slug>/', views.PlaylistTrackView.as_view(), name='playlist-track-remove'),

    re_path(r'^media/audio/(?P<path>.+)$', views.ServeAudioView.as_view(), name='serve-audio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
