from django.db import models
from django.urls import reverse

from django.contrib.gis.db import models as geomodels

from photo_gallery.models import Article
from datetime import datetime, timedelta

def event_date(start, end):
    if end is None or start == end:
        return start.strftime("%d %b %Y")
    elif start.strftime("%b") == end.strftime("%b"):
        return start.strftime("%d") + " - " + end.strftime("%d %b %Y") 
    else:
        return start.strftime("%d %b") + " - " + end.strftime("%d %b %Y")

class Spot(models.Model):
    name = models.CharField(max_length=100, blank=False)
    geometry = geomodels.PointField()

    class Meta:
        # order of drop-down list items
        ordering = ('name',)

        # plural form in admin view
        verbose_name_plural = 'spots'


class DatedSpot(models.Model):
    album = models.ForeignKey(Article, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=256)
    
    start_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=1)

    geom = geomodels.PointField()

    @property
    def popupContent(self):
        popup = '<b>{}</b><br>{}'.format(self.name, event_date(self.start_date, self.end_date))
        if self.album:
            article_link = 'Article : <a href="{}">{}</a>'.format(reverse('photo_gallery:article', args=(self.album.slug,)), self.album.title)
        else:
            article_link = 'Pas d\'article en rapport'
        
        popup += '<br><span class=article-link-popup>{}</span>'.format(article_link)

        popup += '<span class="btn-floating btn-small waves-effect waves-light zoom-in-popup"><i class="fas fa-compress-arrows-alt"></i></span>'

        return popup

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration)    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.album and not self.start_date:
            self.start_date = self.album.start_date
        super(DatedSpot, self).save(*args, **kwargs)

