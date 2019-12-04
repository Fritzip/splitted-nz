#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import DatedSpot, GPXTrack
from photo_gallery.models import Article

from djgeojson.views import GeoJSONLayerView

from django.core.serializers import serialize

class ArticleGeoJSONListView(GeoJSONLayerView):
    def get_queryset(self):
        if self.kwargs['type'] == 'gpx':
            if self.kwargs['slug'] == 'global':
                return GPXTrack.objects.all()
            elif self.kwargs['slug']:
                self.article = get_object_or_404(Article, slug=self.kwargs['slug'])
                return GPXTrack.objects.filter(article=self.article.pk)
            else:
                pass #todo raise error
        elif self.kwargs['type'] == 'sleepspots':
            if self.kwargs['slug'] == 'global':
                return DatedSpot.objects.all().order_by('-start_date')
            elif self.kwargs['slug']:
                self.article = get_object_or_404(Article, slug=self.kwargs['slug'])
                return DatedSpot.objects.filter(article=self.article.pk).order_by('-start_date')
            else:
                pass #todo raise error
        else:
            pass
            # todo raise 404