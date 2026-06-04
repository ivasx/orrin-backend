from rest_framework import serializers

from legal.models import LegalDocument


class LegalDocumentSerializer(serializers.ModelSerializer):
    lastUpdated = serializers.DateField(source='last_updated', read_only=True)

    class Meta:
        model = LegalDocument
        fields = ['title', 'lastUpdated', 'sections']
