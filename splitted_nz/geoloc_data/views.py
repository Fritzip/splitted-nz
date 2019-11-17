#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render
from .models import DatedSpot

def map(request):
    sleepspots_list = DatedSpot.objects.all().order_by('-start_date')
    return render(request, 'geoloc_data/map.html', {'sleepspots': sleepspots_list})
