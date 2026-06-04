from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ListeningHistory, HISTORY_LIMIT


@receiver(post_save, sender=ListeningHistory)
def enforce_history_limit(sender, instance, created, **kwargs):
    """Keep each user's history within HISTORY_LIMIT entries."""
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


@receiver(post_save, sender=ListeningHistory)
def increment_plays_count(sender, instance, created, **kwargs):
    """Atomically increment the denormalised play counter on the track."""
    if not created:
        return

    # F()-expression avoids race conditions without SELECT then UPDATE
    from django.db.models import F
    instance.track.__class__.objects.filter(pk=instance.track_id).update(
        plays_count=F('plays_count') + 1,
    )
