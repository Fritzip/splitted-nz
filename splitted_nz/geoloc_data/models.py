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

class DatedSpot(models.Model):
    album = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=256)
    
    start_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=1)

    geom = geomodels.PointField()

    @property
    def popupContent(self):
        popup = '<i class="fas fa-bed" style="margin:auto 5px;"></i><b>{}</b><br><i class="fas fa-calendar-alt" style="margin:auto 5px;"></i>{}'.format(self.name, event_date(self.start_date, self.end_date))
        
        if self.album:
            popup += '<br><a class="article-link-popup flex-container-row btn btn-small waves-effect waves-light" data-letters="{}" href="{}"><i class="fas fa-newspaper"></i><span style="margin:auto 5px;font-weight:bold">{}</span><i class="fas fa-angle-right"></i></a>'.format(self.album.letters, reverse('photo_gallery:article', args=(self.album.slug,)), self.album.title)

        popup += '<span class=" zoom-in-popup btn-floating btn-small waves-effect waves-light"><i class="fas fa-compress-arrows-alt"></i></span>'

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

