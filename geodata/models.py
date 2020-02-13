from django.db import models

from photo_gallery.models import Article

class DatedSpot(models.Model):
    pass

class GPXTrack(models.Model):
    pass

class StravActivity(models.Model):
    name = models.CharField(max_length=256)
    status = models.CharField( max_length=32, blank=True, null=True )
    average_speed = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    elapsed_time = models.FloatField(blank=True, null=True) # could be int
    elev_high = models.FloatField(blank=True, null=True)
    elev_low = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)
    moving_time = models.FloatField(blank=True, null=True) # could be int
    total_elevation_gain = models.FloatField(blank=True, null=True)
    
    start_date_local = models.DateTimeField(blank=True, null=True)

    total_elevation_gain = models.FloatField(blank=True, null=True)
    moving_time = models.DurationField(blank=True, null=True)
    average_speed = models.FloatField(blank=True, null=True)

    polyline = models.CharField(max_length=2048, blank=True, null=True)

    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name