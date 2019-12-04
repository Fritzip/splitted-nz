# from django.db import models
from django.urls import reverse

from django.contrib.gis.db import models

from photo_gallery.models import Article
from datetime import datetime, timedelta

def event_date(start, end=None):
    if end is None or start == end:
        return start.strftime("%d %b %Y")
    elif start.strftime("%b") == end.strftime("%b"):
        return start.strftime("%d") + " - " + end.strftime("%d %b %Y") 
    else:
        return start.strftime("%d %b") + " - " + end.strftime("%d %b %Y")

def popupheader(title, icon, date, time=None):
    htmltime = ''
    if time:
        htmltime = '<i class="fas fa-clock"></i>{}'.format(time)
    return '''<div class="grid-popup-row">
                        <b style="font-size:14px;">{1}</b>
                   </div>
                   <div class="grid-popup-row" style="justify-content: flex-start;">
                        <i class="fas fa-calendar-alt"></i>
                        {2}{3}
                   </div>'''.format(icon, title, date, htmltime)
                        # <i class="fas {0}" style="font-size:16px;"></i>
                    # <i class="fas {0}" style="visibility:hidden;"></i>

def popuparticlebtn(letters, slug, title):
    return '''<a class="article-link-popup flex-popup-row nowrap btn waves-effect waves-light" data-letters="{}" href="{}">
                            <i class="fas fa-newspaper"></i>
                            <b>{}</b>
                            <i class="fas fa-angle-right"></i>
                        </a>'''.format(letters, reverse('photo_gallery:article', args=(slug,)), title)

class DatedSpot(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=256)
    
    start_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=1)

    wkb_geometry = models.PointField()

    @property
    def popupContent(self):
        popup = popupheader(self.name, "fa-bed", event_date(self.start_date, self.end_date))
        
        if self.article:
            popup += popuparticlebtn(self.article.letters, self.article.slug, self.article.title)

        popup += '<a class="zoom-in-popup btn-floating btn-small waves-effect waves-light"><i class="fas fa-compress-arrows-alt"></i></a>'

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
    HIKE = 'hiking'
    STATUS = (
       (BIKE, 'Bike'),
       (RUN, 'Run'),
       (HIKE, 'Hike'),
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
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    moving_time = models.DurationField(blank=True, null=True)
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

    def get_activity_icon(self):
        if self.status == self.BIKE:
            return "fa-biking"
        elif self.status == self.RUN:
            return "fa-running"
        elif self.status == self.HIKE:
            return "fa-hiking"
        else:
            return "fa-question"

    def get_formated_date(self, datetime):
        return datetime.strftime("%d/%m") if datetime else ""

    def get_formated_time(self, datetime):
        return datetime.strftime("%H:%M") if datetime else ""

    @property
    def popupContent(self):
        popup = popupheader(self.name, self.get_activity_icon(), event_date(self.start_date), self.get_formated_time(self.start_date))

        popup += '''<div class="flex-popup-row">
                        <div class="card-panel flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                        <div class="card-panel flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                    </div>
                    <div class="flex-popup-row">
                        <div class="card-panel flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                        <div class="card-panel flex-popup-col">
                          <i class="fas {}"></i>{}
                        </div>
                    </div>
                '''.format( "fa-arrow-up", self.get_formated_stat(self.elevation_gain, "m"),
                            "fa-ruler-horizontal", self.get_formated_stat(self.distance, "km"),
                            "fa-stopwatch", self.get_formated_stat(self.moving_time, ""),
                            "fa-tachometer-alt", self.get_formated_stat(self.avg_speed, "km/h"))
        
        if self.article:
            popup += popuparticlebtn(self.article.letters,self.article.slug,self.article.title) 
            
        popup += '<span class="top-left btn-floating btn-small red" style="cursor: default;"><i class="fas {}"></i></span>'.format(self.get_activity_icon())

        return popup

class GPXFile(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=256)


