from django.shortcuts import render
from django.views.generic import TemplateView

from orrin.models import Track


# Create your views here.
class HomeView(TemplateView):
    template_name = 'orrin/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Track.objects.all()[:20]
        return context


class TrackDetailView(TemplateView):
    model = Track

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context