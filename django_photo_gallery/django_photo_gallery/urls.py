from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin

# from app.models import SleepSpot
from djgeojson.views import GeoJSONLayerView

admin.autodiscover()

app_name = "splittednz"

urlpatterns = [
    # Gallery
    url(r'^$', app.views.gallery, name='gallery'),
    # Article detail
    url(r'^(?P<slug>[-\w]+)$', app.views.ArticleDetail.as_view(), name='article'), 
    #template_name='article.html'

    # Map
    url(r'^map/$', app.views.map, name='map'),
    #url(r'^data.geojson$', GeoJSONLayerView.as_view(model=SleepSpot, properties=('title', 'album_title', 'event_date', 'slug')), name='data'),

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

handler404 = 'app.views.handler404'




