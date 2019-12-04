from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'photo_gallery'

urlpatterns = [
    # Gallery
    # url(r'^$', views.gallery, name='gallery'),
    path('', views.gallery, name='gallery'),

    # Article detail
    # url(r'^(?P<slug>[-\w]+)$', views.ArticleDetail.as_view(), name='article'), 
    path('<slug>', views.ArticleDetail.as_view(), name='article'), 

    # Map
    #url(r'^map/$', views.map, name='map'),
]