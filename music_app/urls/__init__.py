from django.contrib import admin
from django.urls import path, include
from . import auth, swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orrin.urls')),
    path('', include(auth.urlpatterns)),
    path('', include(swagger.urlpatterns))
]