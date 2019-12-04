from .models import DatedSpot, GPXTrack
 # RoutePoints, Routes, TrackPoints, Waypoints
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class DatedSpotResource(resources.ModelResource):
    class Meta:
        model = DatedSpot

class DatedSpotAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'duration', 'article')
    ordering = ('-start_date',)
    resource_class = DatedSpotResource

# register models in the admin site
admin.site.register(DatedSpot, DatedSpotAdmin)


# admin.site.register(RoutePoints, admin.GeoModelAdmin)
# admin.site.register(Routes, admin.GeoModelAdmin)
admin.site.register(GPXTrack, admin.GeoModelAdmin)
# admin.site.register(TrackPoints, admin.GeoModelAdmin)
# admin.site.register(Waypoints, admin.GeoModelAdmin)
