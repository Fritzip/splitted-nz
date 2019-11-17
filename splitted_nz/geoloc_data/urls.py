from django.conf.urls import url
from . import views

app_name = 'geoloc_data'

urlpatterns = [
    # city detail view
    url(r'^city/(?P<pk>[0-9]+)$', views.SpotsDetailView.as_view(), name='city-detail'),

    url(r'^maptemp/$', views.map, name='maptemp'),
]