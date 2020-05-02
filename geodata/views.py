#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render

from .models import SleepSpot, StravActivity
from datetime import date, datetime

def map(request):
    # start = min(datetime.combine(SleepSpot.objects.earliest('start_date').start_date, datetime.min.time()),  StravActivity.objects.earliest('start_date_local').start_date_local)
    # end = max(datetime.combine(SleepSpot.objects.latest('start_date').start_date, datetime.min.time()), StravActivity.objects.latest('start_date_local').start_date_local)
    date_range = [str(date(2019, 10, 1)), str(date.today())]
    sleepspots_list = SleepSpot.objects.all().order_by('-start_date')
    tracks_list = StravActivity.objects.filter(start_date_local__gt = date_range[0])#.order_by('-start_date')
    return render(request, 'geodata/map.html', {'sleepspots': sleepspots_list, 'tracks': tracks_list, 'date_range': date_range})
