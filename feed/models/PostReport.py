from django.conf import settings
from django.db import models


class PostReport(models.Model):
    REASON_CHOICES = (
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_reports',
    )
    post = models.ForeignKey(
        'feed.Post',
        on_delete=models.CASCADE,
        related_name='reports',
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
