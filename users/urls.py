from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import (
    RegisterView,
    GoogleLoginView,
    CurrentUserProfileView,
    UserProfileDetailView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),

    path('me/', CurrentUserProfileView.as_view(), name='current_user_profile'),
    path('<str:username>/', UserProfileDetailView.as_view(), name='user_profile_detail'),
]