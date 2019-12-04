# from django.db import models
from django.urls import reverse

from django.contrib.gis.db import models

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
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=256)
    
    start_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=1)

    wkb_geometry = models.PointField()

    @property
    def popupContent(self):
        popup = '''<div class="grid-popup-row">
                        <i class="fas {}"></i>
                        <b>{}</b>
                        <i class="fas {}" style="visibility:hidden;"></i>
                   </div>
                   <div class="grid-popup-row" style="justify-content: flex-start;">
                        <i class="fas {}"></i>
                        {}
                   </div>'''.format("fa-bed", self.name, "fa-bed", "fa-calendar-alt", event_date(self.start_date, self.end_date))
        
        if self.article:
            popup += '''<a class="article-link-popup flex-popup-row btn waves-effect waves-light" data-letters="{}" href="{}">
                            <i class="fas fa-newspaper"></i>
                            <b>{}</b>
                            <i class="fas fa-angle-right"></i>
                        </a>'''.format(self.article.letters, reverse('photo_gallery:article', args=(self.article.slug,)), self.article.title)

        popup += '<a class=" zoom-in-popup btn-floating btn-small waves-effect waves-light"><i class="fas fa-compress-arrows-alt"></i></a>'

        return popup

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration)    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.article and not self.start_date:
            self.start_date = self.article.start_date
        super(DatedSpot, self).save(*args, **kwargs)


class GPXTrack(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True, unique=True)
    type = models.CharField(max_length=256, blank=True, null=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)

    BIKE = 'biking'
    RUN = 'running'
    HIKE = 'hicking'
    STATUS = (
       (BIKE, 'Mountain biking'),
       (RUN, 'Trail run'),
       (HIKE, 'Hicking'),
    )
    status = models.CharField(
       max_length=32,
       choices=STATUS,
       default=BIKE,
       blank=True,
       null=True
    )
    elevation_gain = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    moving_time = models.TimeField(blank=True, null=True)
    avg_speed = models.FloatField(blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'tracks'

    def get_formated_stat(self, field, unit):
        if field:
            return "{} {}".format(field, unit)
        else:
            return "-"

    @property
    def popupContent(self):
        popup = '''<div>
                    <div class="flex-popup-row">
                        <i class="fas {}"></i><b>{}</b><i class="fas {}"></i>
                    </div>
                    <div class="flex-popup-row">
                        <div class="flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                        <div class="flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                    </div>
                    <div class="flex-popup-row">
                        <div class="flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                        <div class="flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                        <div class="flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                    </div>
                '''.format( "fa-biking", self.name, "fa-route",
                            "fa-arrow-up", self.get_formated_stat(self.elevation_gain, "m"),
                            "fa-ruler-horizontal", self.get_formated_stat(self.distance, "km"),
                            "fa-hourglass-start", self.get_formated_stat(self.start_time, ""),
                            "fa-stopwatch", self.get_formated_stat(self.moving_time, ""),
                            "fa-hourglass-end", self.get_formated_stat(self.end_time, ""),
                            "fa-tachometer-alt", self.get_formated_stat(self.avg_speed, "km/h"))
                
        
        if self.article:
            popup += '''<a class="article-link-popup flex-popup-row btn waves-effect waves-light" data-letters="{}" href="{}">
                                <i class="fas fa-newspaper"></i><b>{}</b><i class="fas fa-angle-right"></i>
                            </a>'''.format(self.article.letters, reverse('photo_gallery:article', args=(self.article.slug,)), self.article.title)

        popup += '</div>'
        # popup += '<span class=" zoom-in-popup btn-floating btn-small waves-effect waves-light"><i class="fas fa-compress-arrows-alt"></i></span>'

        return popup

class GPXFile(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=256)


