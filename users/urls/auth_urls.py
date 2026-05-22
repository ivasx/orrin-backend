from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import GoogleLoginView, RegisterView

urlpatterns = [
    path('token/', extend_schema(tags=['Auth'])(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', extend_schema(tags=['Auth'])(TokenRefreshView.as_view()), name='token_refresh'),
    path('token/verify/', extend_schema(tags=['Auth'])(TokenVerifyView.as_view()), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
]