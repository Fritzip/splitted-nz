#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from photo_gallery.models import Article, ArticleImage
from geodata.models import StravActivity, SleepSpot

import json

def gallery(request):
    articles_list = Article.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(articles_list, 9)

    page = request.GET.get('page')
    try:
        articles_p = paginator.page(page)
    except PageNotAnInteger:
        articles_p = paginator.page(1)
        # If page is not an integer, deliver first page.
    except EmptyPage:
        articles_p = paginator.page(paginator.num_pages) 
        # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'photo_gallery/gallery.html', {'articles':articles_list})

# def map(request):
#     sleepspots_list = SleepSpot.objects.all().order_by('-start_date')
#     return render(request, 'photo_gallery/map.html', {'sleepspots': sleepspots_list})

# from django.core.serializers import serialize

class ArticleDetail(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = ArticleImage.objects.filter(album=self.object.id).order_by('alt')

        #json.dumps(list(
        context['stravactivities'] = list(StravActivity.objects.filter(article=self.object.id))

        context['sleepspots'] = SleepSpot.objects.filter(article=self.object.id).order_by('-start_date')

        try:
            next_article = self.object.get_next_by_start_date().slug
        except Article.DoesNotExist:
            next_article = None

        try:
            prev_article = self.object.get_previous_by_start_date().slug
        except Article.DoesNotExist:
            prev_article = None
            
        context['next'] = next_article
        context['prev'] = prev_article

        return context

def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'photo_gallery/handler404.html', None, None, 404)

def unavailable(request):
    return render(request, 'photo_gallery/article_detail.html')
