from django.urls import path

from users.views import (
    CurrentUserProfileView,
    UserProfileDetailView,
    ToggleFollowView,
    UserFollowersView,
    UserFollowingView,
    UserPostsView,
    UserSearchView,
)

urlpatterns = [
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('me/', CurrentUserProfileView.as_view(), name='user-me'),
    path('<str:username>/', UserProfileDetailView.as_view(), name='user-profile'),
    path('<str:username>/follow/', ToggleFollowView.as_view(), name='user-follow'),
    path('<str:username>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('<str:username>/following/', UserFollowingView.as_view(), name='user-following'),
    path('<str:username>/posts/', UserPostsView.as_view(), name='user-posts'),
]