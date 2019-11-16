from django.views.generic import DetailView
from .models import Spot


class SpotsDetailView(DetailView):
    """
        Spot detail view.
    """
    template_name = 'geoloc_data/city-detail.html'
    model = Spot