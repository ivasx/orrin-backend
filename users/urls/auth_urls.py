from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import GoogleLoginView, RegisterView
from users.views.PasswordResetViews import PasswordResetView, PasswordResetConfirmView
from users.views.TokenView import EmailOrUsernameTokenObtainPairView


@extend_schema(tags=['Auth'])
class DecoratedTokenRefreshView(TokenRefreshView): pass

@extend_schema(tags=['Auth'])
class DecoratedTokenVerifyView(TokenVerifyView): pass

urlpatterns = [
    path('token/', EmailOrUsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]