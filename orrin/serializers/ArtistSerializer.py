from rest_framework import serializers
from ..models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'name',
            'slug',
            'type',
            'genres',
            'about',
            'history',
            'location',
            'join_date',
            'monthly_listeners',
            'image',
            'socials',
        )