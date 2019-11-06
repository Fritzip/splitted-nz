#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from app.models import Article, ArticleImage, SleepSpot

def gallery(request):
    articles_list = Article.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(articles_list, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
        # If page is not an integer, deliver first page.
    except EmptyPage:
        articles = paginator.page(paginator.num_pages) 
        # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'gallery.html', { 'articles': articles_list })

def map(request):
    sleepspots_list = SleepSpot.objects.all().order_by('-start_date')
    return render(request, 'map.html', {'sleepspots': sleepspots_list})

class ArticleDetail(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = ArticleImage.objects.filter(album=self.object.id)
        context['sleepspots'] = SleepSpot.objects.filter(album=self.object.id).order_by('-start_date')
        return context

def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)
