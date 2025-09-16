from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from music_app import settings
from . import views
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)