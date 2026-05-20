from django.urls import path

from .views import TopTracksView, TopArtistsView, TopAlbumsView

urlpatterns = [
    path('stats/top-tracks/', TopTracksView.as_view(), name='stats-top-tracks'),
    path('stats/top-albums/', TopAlbumsView.as_view(), name='stats-top-albums'),
    path('stats/top-artists/', TopArtistsView.as_view(), name='stats-top-artists'),
]
