from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^', include('photo_gallery.urls')),
    url(r'^', include('geodata.urls')),

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




