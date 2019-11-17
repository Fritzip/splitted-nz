#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Spot, DatedSpot


class SpotsDetailView(DetailView):
    """
        Spot detail view.
    """
    # template_name = 'geoloc_data/city-detail.html'
    model = Spot


def map(request):
    sleepspots_list = DatedSpot.objects.all().order_by('-start_date')
    return render(request, 'geoloc_data/city-detail.html', {'sleepspots': sleepspots_list})
