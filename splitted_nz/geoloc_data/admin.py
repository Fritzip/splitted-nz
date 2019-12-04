from .models import DatedSpot, GPXTrack
 # RoutePoints, Routes, TrackPoints, Waypoints
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "d M Y - H:i"

class DatedSpotResource(resources.ModelResource):
    class Meta:
        model = DatedSpot

class DatedSpotAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'duration', 'article')
    ordering = ('-start_date',)
    resource_class = DatedSpotResource

admin.site.register(DatedSpot, DatedSpotAdmin)

class GPXTrackResource(resources.ModelResource):
    class Meta:
        model = GPXTrack

class GPXTrackAdmin(ImportExportModelAdmin):
    list_display = ('name', 'status', 'start_date', 'distance', 'article')
    list_filter = ('start_date', 'status')
    ordering = ('-start_date',)
    resource_class = GPXTrackResource

admin.site.register(GPXTrack, GPXTrackAdmin)
