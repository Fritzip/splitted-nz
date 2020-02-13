from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .models import StravActivity

import photo_gallery

app_name = 'geodata'

urlpatterns = [
    # city detail view
    #url(r'^city/(?P<pk>[0-9]+)$', views.SpotsDetailView.as_view(), name='city-detail'),

    path('map/', views.map, name='map'),
    # path('map/', photo_gallery.views.unavailable, name='map'),
    # path('map/', TemplateView.as_view(template_name='geodata/map.html'), name='map'),
    # path('map/', TemplateView.as_view(template_name='geodata/map.html'), name='map'),
]