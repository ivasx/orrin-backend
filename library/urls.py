from django.urls import path

from library.views import (
    LikedTracksView,
    TrackLikeToggleView,
    FollowedArtistsView,
    ArtistFollowToggleView,
    ListeningHistoryView,
    ListeningHistoryEntryView,
    FriendsActivityView,
    SavedAlbumsView,
    AlbumSaveToggleView,
    LibraryView,
)
from library.views.FavoritesView import FavoritesView

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('library/liked/', LikedTracksView.as_view(), name='library-liked'),
    path('library/artists/', FollowedArtistsView.as_view(), name='library-artists'),
    path('library/albums/', SavedAlbumsView.as_view(), name='library-albums'),
    path('library/albums/<slug:slug>/save/', AlbumSaveToggleView.as_view(), name='album-save'),

    path('favorites/', FavoritesView.as_view(), name='favorites'),

    path('history/', ListeningHistoryView.as_view(), name='history-list'),
    path('history/<int:pk>/', ListeningHistoryEntryView.as_view(), name='history-entry'),

    path('friends/activity/', FriendsActivityView.as_view(), name='friends-activity'),

    path('tracks/<slug:slug>/like/', TrackLikeToggleView.as_view(), name='track-like'),
    path('artists/<slug:slug>/follow/', ArtistFollowToggleView.as_view(), name='artist-follow'),
]
