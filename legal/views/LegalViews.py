from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from legal.models import LegalDocument
from legal.serializers.LegalSerializer import LegalDocumentSerializer

_SUPPORTED_LANGUAGES = {choice[0] for choice in LegalDocument.LANGUAGE_CHOICES}
_DEFAULT_LANGUAGE = 'en'


def _get_language(request):
    lang = request.query_params.get('lang', _DEFAULT_LANGUAGE).lower()
    return lang if lang in _SUPPORTED_LANGUAGES else _DEFAULT_LANGUAGE


class LegalDocumentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    _doc_type: str  # set by subclasses

    @extend_schema(
        tags=['Legal'],
        parameters=[
            OpenApiParameter(
                name='lang',
                description='Language code (en, uk). Defaults to en.',
                required=False,
                type=str,
            )
        ],
    )
    def get(self, request):
        language = _get_language(request)
        doc = (
            LegalDocument.objects
            .filter(doc_type=self._doc_type, language=language, is_active=True)
            .first()
        )
        if doc is None:
            return Response(
                {'detail': 'Document not available.'},
                status=404,
            )
        return Response(LegalDocumentSerializer(doc).data)


class TermsView(LegalDocumentView):
    _doc_type = 'terms'


class PrivacyView(LegalDocumentView):
    _doc_type = 'privacy'
