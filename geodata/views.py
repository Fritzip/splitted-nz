#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render

from .models import SleepSpot, StravActivity
from datetime import date

def map(request):
    sleepspots_list = SleepSpot.objects.all().order_by('-start_date')
    tracks_list = StravActivity.objects.filter(start_date_local__gt = date(2019, 9, 30))#.order_by('-start_date')
    return render(request, 'geodata/map.html', {'sleepspots': sleepspots_list, 'tracks': tracks_list})
