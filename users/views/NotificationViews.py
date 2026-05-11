from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Notification
from users.serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = (
            Notification.objects
            .filter(recipient=request.user)
            .select_related("actor")
        )
        serializer = NotificationSerializer(
            notifications,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user,
        )
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return Response(
            NotificationSerializer(notification, context={"request": request}).data
        )


class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
