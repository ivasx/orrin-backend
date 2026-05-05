from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ListeningHistory, HISTORY_LIMIT


@receiver(post_save, sender=ListeningHistory)
def enforce_history_limit(sender, instance, created, **kwargs):
    if not created:
        return

    overflow_ids = (
        ListeningHistory.objects
        .filter(user=instance.user)
        .order_by('-played_at')
        .values_list('id', flat=True)[HISTORY_LIMIT:]
    )

    if overflow_ids:
        ListeningHistory.objects.filter(id__in=list(overflow_ids)).delete()
