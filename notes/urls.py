from django.urls import path

from notes.views.NoteViews import (
    TrackNotesView,
    ArtistNotesView,
    NoteDetailView,
    NoteLikeView,
)

urlpatterns = [
    path('tracks/<slug:slug>/notes/', TrackNotesView.as_view(), name='track-notes'),
    path('artists/<slug:slug>/notes/', ArtistNotesView.as_view(), name='artist-notes'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/like/', NoteLikeView.as_view(), name='note-like'),
]
