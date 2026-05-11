from django.urls import path

from users.views import (
    NotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
    path("read-all/", MarkAllNotificationsReadView.as_view(), name="notification-read-all"),
]
