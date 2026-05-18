from django.urls import path

from feed.views import (
    FeedView,
    PostDetailView,
    PostLikeView,
    PostRepostView,
    PostSaveView,
    PostReportView,
    PostCommentView,
    ArtistPostsView,
)

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed-list'),
    path('feed/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('feed/posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('feed/posts/<int:pk>/repost/', PostRepostView.as_view(), name='post-repost'),
    path('feed/posts/<int:pk>/save/', PostSaveView.as_view(), name='post-save'),
    path('feed/posts/<int:pk>/report/', PostReportView.as_view(), name='post-report'),
    path('feed/posts/<int:pk>/comments/', PostCommentView.as_view(), name='post-comments'),
    path('artists/<slug:slug>/posts/', ArtistPostsView.as_view(), name='artist-posts'),
]
