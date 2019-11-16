from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

import photo_gallery.forms
import photo_gallery.views

from django.conf.urls import include
from django.contrib import admin

# from photo_gallery.models import SleepSpot
from djgeojson.views import GeoJSONLayerView

admin.autodiscover()

urlpatterns = [
    # Gallery
    url(r'^$', photo_gallery.views.gallery, name='gallery'),
    # Article detail
    url(r'^(?P<slug>[-\w]+)$', photo_gallery.views.ArticleDetail.as_view(), name='article'), 
    #template_name='article.html'

    # Map
    url(r'^map/$', photo_gallery.views.map, name='map'),
    #url(r'^data.geojson$', GeoJSONLayerView.as_view(model=SleepSpot, properties=('title', 'album_title', 'event_date', 'slug')), name='data'),
    
    # url(r'^cities/', include('geoloc_data.urls')),

    # Favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
     
    # Auth related urls
    url(r'^accounts/login/$', views.LoginView, name='login'),
    url(r'^logout$', views.LogoutView, { 'next_page': '/', }, name='logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'photo_gallery.views.handler404'




