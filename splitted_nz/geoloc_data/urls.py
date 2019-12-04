from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .models import GPXTrack

app_name = 'geoloc_data'

urlpatterns = [
    # city detail view
    #url(r'^city/(?P<pk>[0-9]+)$', views.SpotsDetailView.as_view(), name='city-detail'),

    # url(r'^map/$', views.map, name='map'),
    # path('map/', views.map, name='map'),
    path('map/', TemplateView.as_view(template_name='geoloc_data/map.html'), name='map'),

    path('<slug:slug>/<str:type>.geojson', views.ArticleGeoJSONListView.as_view(model=GPXTrack, geometry_field="wkb_geometry",  properties=('name','popupContent',)), name='gpxtrack'), 

    # url(r'^data.geojson$', GeoJSONLayerView.as_view(model=GPXTrack, geometry_field="wkb_geometry",  properties=('name','popupContent',)), name='gpxtrack'),

    # path('data.geojson/<slug:slug>', GeoJSONLayerView.as_view(model=GPXTrack, geometry_field="wkb_geometry",  properties=('name','popupContent',)), name='gpxtrack'),

]