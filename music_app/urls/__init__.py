from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('orrin.urls')),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/docs/', include('music_app.urls.swagger')),
]