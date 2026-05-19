from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('orrin.urls')),
    path('api/v1/', include('library.urls')),
    path('api/v1/', include('chat.urls')),
    path('api/v1/auth/', include('users.urls.auth_urls')),
    path('api/v1/users/', include('users.urls.users')),
    path('api/notifications/', include('users.urls.notifications')),
    path('api/v1/', include('feed.urls')),
    path('api/v1/docs/', include('music_app.urls.swagger')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
