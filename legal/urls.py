from django.urls import path

from legal.views.LegalViews import TermsView, PrivacyView

urlpatterns = [
    path('legal/terms/', TermsView.as_view(), name='legal-terms'),
    path('legal/privacy/', PrivacyView.as_view(), name='legal-privacy'),
]
