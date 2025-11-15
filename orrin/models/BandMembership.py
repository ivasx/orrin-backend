from django.db import models
from ..models import Artist


class BandMembership(models.Model):
    """
    Represents a relationship between an artist and a music group.
    """

    member = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='band_memberships',
        limit_choices_to={'type': 'person'}, verbose_name='Artist'
    )

    group = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='members',
        limit_choices_to={'type': 'group'}, verbose_name='Music group'
    )

    role = models.CharField(max_length=255, verbose_name='Role')

    join_date = models.DateField(verbose_name='Join date', blank=True, null=True)
    leave_date = models.DateField(verbose_name='Leave date', blank=True, null=True)

    class Meta:
        unique_together = ('member', 'group')

    def __str__(self):
        return f'{self.member.name} - {self.role} in {self.group}'